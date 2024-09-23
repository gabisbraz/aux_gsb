import pandas as pd
import numpy as np
import streamlit as st
from streamlit_dynamic_filters import DynamicFilters
from app.utils.charts.waterfall import create_waterfall_chart
from streamlit_extras.dataframe_explorer import dataframe_explorer

# Configurações
num_rows_1 = 3000
num_rows_2 = 1000

# Listas de exemplos para as colunas UF e MUNICIPIO
ufs = ["SP", "RJ", "MG", "ES", "BA", "PR", "SC", "RS", "GO", "DF"]
municipios = [
    "São Paulo",
    "Rio de Janeiro",
    "Belo Horizonte",
    "Vitória",
    "Salvador",
    "Curitiba",
    "Florianópolis",
    "Porto Alegre",
    "Goiânia",
    "Brasília",
]

# Gerar DataFrame 1
df_base_unica = pd.DataFrame(
    {
        "CD_PONTO": [i for i in range(1, num_rows_1 + 1)],
        "UF": np.random.choice(ufs, num_rows_1),
        "MUNICIPIO": np.random.choice(municipios, num_rows_1),
        "DICOM": np.random.randint(1, 6, num_rows_1),
        "REGCOM": np.random.randint(1, 6, num_rows_1),
        "FOOTPRINT": np.random.choice(["Sim", "Não"], num_rows_1),
    }
)

# Gerar DataFrame 2
df_acompanhamento_esteira = pd.DataFrame(
    {
        "AGENCIA": [i for i in range(1, num_rows_2 + 1)],
        "UF": np.random.choice(ufs, num_rows_2),
        "MUNICIPIO": np.random.choice(municipios, num_rows_2),
        "DINEG": np.random.randint(1, 6, num_rows_2),
        "REGCOM": np.random.randint(1, 6, num_rows_2),
        "STATUS CONSOLIDADO": np.random.choice(
            ["a", "b", "c", "d", "e", "f"], num_rows_2
        ),
        "ESTEIRA": np.random.choice(["a", "b", "c", "d", "e", "f"], num_rows_2),
    }
)


def calcula_valores_barras_waterfall_chart(
    df_filtered_copy: pd.DataFrame,
    df_cria_waterfall_chart: pd.DataFrame,
):
    """_summary_

    Args:
        df_filtered_copy (pd.DataFrame): _description_
        df_cria_waterfall_chart (pd.DataFrame): _description_

    Returns:
        _type_: _description_
    """

    # GET QTD. DE AGÊNCIAS (BASE 360) RESUTANTES DO FILTRO
    qtd_agencias_result_filtro = int(len(df_filtered_copy))

    # GET QTD. DE AGÊNCIAS QUE ESTÃO NA ESTEIRA
    qtd_agencias_em_esteira = int(
        len(df_filtered_copy.loc[df_filtered_copy["ESTEIRA"] != "-"])
    )

    # LISTA DE CATEGORIAS DE ESTEIRA
    list_categorias_esteiras = list(
        df_cria_waterfall_chart["STATUS CONSOLIDADO"].unique()
    )
    # LISTA DE QTD. DE AGÊNCIAS EM CADA ESTEIRA
    list_qtd_agencias_em_esteira = list(df_cria_waterfall_chart["AGENCIA"].unique())

    # CRIA LISTA DE CATEGORIAS DO EIXO X PARA O GRÁFICO
    list_eixo_x = [
        "TOTAL DE AGÊNCIAS DO PARQUE",
        "AGÊNCIAS EM ESTEIRA",
    ] + list_categorias_esteiras

    # CRIA BARRA DE TOTAL DE AGÊNCIAS
    total_agencias_data = [qtd_agencias_result_filtro] + [
        "-" for _ in range(len(list_categorias_esteiras) + 1)
    ]

    # CRIA BARRA DE ESTEIRAS
    esteira_data = ["-", qtd_agencias_em_esteira] + [
        int(i) for i in list_qtd_agencias_em_esteira
    ]

    # LISTA AUXILIAR PARA ACUMULAR DADOS NO GRÁFICO
    aux = []
    for qtd_agencias in list_qtd_agencias_em_esteira:
        qtd_agencias_em_esteira -= int(qtd_agencias)
        aux.append(int(qtd_agencias_em_esteira))

    # DADOS AUXILIARES PARA O GRÁFICO WATERFALL
    auxiliary_data = ["-", "-"] + aux

    return list_eixo_x, auxiliary_data, total_agencias_data, esteira_data


def main_page_esteira_agencias(user_configs: dict = {}):

    # CONFIGURAÇÃO DO PANDAS STYLER
    pd.set_option("styler.render.max_elements", 500000)

    # ! LEITURA DA BASE360
    # ! LEITURA DA BASE DE ACOMPANHAMENTO DE ESTEIRAS

    # TÍTULO DA PÁGINA
    st.markdown("## Acompanhamento de Esteiras")

    # MERGE DOS DFS BASES360 E ACOMPANAHMENTO DE ESTEIRAS COM BASE NAS COLUNAS "CD_PONTO" E "AGENCIA"
    df_base360_esteira = pd.merge(
        df_base_unica,
        df_acompanhamento_esteira,
        left_on="CD_PONTO",
        right_on="AGENCIA",
        how="outer",
        suffixes=["", "_AC_ESTEIRAS"],
    )

    # TRATATIVAS DE FORMATAÇÃO
    df_base360_esteira = df_base360_esteira.fillna("-")
    df_base360_esteira = df_base360_esteira.astype(str)

    #########################################################################################################

    # SUBTÍTULO - FILTROS DINÂMICOS
    st.markdown("### 1. Selecione os filtros desejados")

    # LISTA DE COLUNAS PARA FILTROS DINÂMICOS
    list_filters_selectbox = ["DINEG", "REGCOM", "UF", "MUNICIPIO", "ESTEIRA"]

    # CRIA OS FILTROS DINÂMICOS COM AS COLUNAS ESPECIFICADAS
    dynamic_filters = DynamicFilters(df_base360_esteira, filters=list_filters_selectbox)

    # EXIBE OS FILTROS
    dynamic_filters.display_filters(
        location="columns", num_columns=len(list_filters_selectbox)
    )

    #########################################################################################################

    # APLICA OS FILTROS SELECIONADOS NO DATAFRAME
    df_filtered = dynamic_filters.filter_df()

    # CÓPIA DO DF FILTRADO PARA MANIPULAÇÃO
    df_filtered_copy = df_filtered.copy()

    # AGRUPA AS AGÊNCIAS POR "STATUS CONSOLIDADO" E FAZ A CONTAGEM
    df_cria_waterfall_chart = (
        df_filtered_copy[["AGENCIA", "STATUS CONSOLIDADO"]]
        .groupby(["STATUS CONSOLIDADO"])
        .count()
        .reset_index()
        .sort_values(by="AGENCIA", ascending=False)
    )

    # * ESPERANDO VALIDAÇÃO DA VIRGINIA
    df_cria_waterfall_chart["STATUS CONSOLIDADO"] = df_cria_waterfall_chart[
        "STATUS CONSOLIDADO"
    ].replace("0", "OUTRO")

    # CALCULA OS VALORES QUE COMPOEM O WATERFALL CHART
    list_eixo_x, auxiliary_data, total_agencias_data, esteira_data = (
        calcula_valores_barras_waterfall_chart(
            df_filtered_copy, df_cria_waterfall_chart
        )
    )

    # SUBTÍTULO PARA O GRÁFICO DE WATERFALL
    st.markdown("### 2. Visualize o resumo das Esteiras do Parque")

    # RENDERIZA GRÁFICO WATERFALL
    create_waterfall_chart(
        list_eixo_x, auxiliary_data, total_agencias_data, esteira_data
    )

    #########################################################################################################

    # SUBTÍTULO PARA BASE DAS ESTEIRAS
    st.markdown("### 3. Veja a Base com detalhamento das Esteiras")

    # SELECIONAR AGÊNCIAS PARA FILTRAR BASE DE ACOMPANHAMENTO DE ESTEIRA
    agencia_selected = st.multiselect(
        "Selecione a Agência que deseja visualizar",
        options=df_acompanhamento_esteira["AGENCIA"].unique(),
        max_selections=1,
        placeholder="Selecione uma Agência",
    )

    # SE ALGUMA AGÊNCIA FOR SELECIONADA, FILTRA OS DADOS DESSA AGÊNCIA
    if agencia_selected:
        df_acompanhamento_esteira_filtered = df_acompanhamento_esteira.loc[
            df_acompanhamento_esteira["AGENCIA"].isin(agencia_selected)
        ]
    else:
        df_acompanhamento_esteira_filtered = df_acompanhamento_esteira

    # EXIBE O DATAFRAME FILTRADO EM FORMATO NÃO EDITÁVEL
    st.data_editor(
        df_acompanhamento_esteira_filtered,
        hide_index=True,
        use_container_width=True,
        disabled=True,
    )

    #########################################################################################################

    # SUBTÍTULO --> BASE 360
    st.markdown("### 4. Visualize a Base 360")

    # EXPANDER PARA OCULTAR/EXIBIR A BASE 360
    with st.expander("BASE 360"):

        # BASE 360 NO DATAFRAME EXPLORER
        st.data_editor(
            dataframe_explorer(df_base_unica),
            hide_index=True,
            use_container_width=True,
            disabled=True,
        )


main_page_esteira_agencias({})
