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
df1 = pd.DataFrame(
    {
        "CD_PONTO": [i for i in range(1, num_rows_1 + 1)],
        "UF": np.random.choice(ufs, num_rows_1),
        "MUNICIPIO": np.random.choice(municipios, num_rows_1),
        "DICOM": np.random.randint(1, 6, num_rows_1),
        "REGCOM": np.random.randint(1, 6, num_rows_1),
        "STATUS": np.random.choice(["Sim", "Não"], num_rows_1),
    }
)

# Gerar DataFrame 2
df2 = pd.DataFrame(
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


# st.dataframe(df1, use_container_width=True, hide_index=True)
# st.dataframe(df2, use_container_width=True, hide_index=True)


# DEFINIÇÃO DA FUNÇÃO PRINCIPAL QUE GERA A PÁGINA "ESTEIRA AGENCIAS" NO STREAMLIT.
def main_page_esteira_agencias(user_configs: dict = {}):

    # DEFINE UMA CONFIGURAÇÃO DO PANDAS PARA RENDERIZAR ATÉ 500 MIL ELEMENTOS NO STYLER (PARA EXIBIÇÃO).
    # ESSA CONFIGURAÇÃO É ÚTIL PARA EXIBIÇÕES EM GRANDES DATAFRAMES
    pd.set_option("styler.render.max_elements", 500000)

    # EXIBE UM TÍTULO NA PÁGINA DO STREAMLIT.
    st.markdown("## Acompanhamento de Esteiras")

    # REALIZA UM MERGE (JUNÇÃO) ENTRE OS DATAFRAMES `df1` E `df2` COM BASE NAS COLUNAS "CD_PONTO" E "AGENCIA".
    # O MÉTODO `how="outer"` GARANTE QUE TODOS OS REGISTROS SEJAM MANTIDOS, MESMO QUE NÃO HAJA CORRESPONDÊNCIA.
    df_acompanhamento_esteira = pd.merge(
        df1,
        df2,
        left_on="CD_PONTO",
        right_on="AGENCIA",
        how="outer",
        suffixes=[
            "",
            "_AC_ESTEIRAS",
        ],  # ADICIONA SUFIXOS PARA DIFERENCIAR COLUNAS COM O MESMO NOME
    )

    # SUBSTITUI VALORES NULOS (NaN) NO DATAFRAME POR "-"
    df_acompanhamento_esteira = df_acompanhamento_esteira.fillna("-")

    # CONVERTE TODO O DATAFRAME PARA O TIPO STRING, O QUE AJUDA NA EXIBIÇÃO E TRATAMENTO DOS DADOS
    df_acompanhamento_esteira = df_acompanhamento_esteira.astype(str)

    # LISTA DE COLUNAS QUE SERÃO USADAS PARA GERAR FILTROS DINÂMICOS NA TELA DO STREAMLIT
    list_filters_selectbox = [
        "DINEG",  # COLUNA QUE REPRESENTA O DINEG, UM INDICADOR
        "REGCOM",  # COLUNA QUE REPRESENTA O REGCOM, OUTRO INDICADOR
        "UF",  # UNIDADE FEDERATIVA, REPRESENTANDO O ESTADO
        "MUNICIPIO",  # MUNICÍPIO ASSOCIADO À AGÊNCIA OU PONTO
        "ESTEIRA",  # COLUNA QUE REPRESENTA A CATEGORIA "ESTEIRA"
    ]

    # CRIA OS FILTROS DINÂMICOS UTILIZANDO A BIBLIOTECA `DynamicFilters` COM AS COLUNAS ESPECIFICADAS.
    # ESSES FILTROS PERMITEM QUE O USUÁRIO FAÇA SELEÇÕES INTERATIVAS DOS DADOS QUE DESEJA VISUALIZAR
    dynamic_filters = DynamicFilters(
        df_acompanhamento_esteira, filters=list_filters_selectbox
    )

    # EXIBE UM SUBTÍTULO NA TELA, SOLICITANDO AO USUÁRIO QUE SELECIONE FILTROS
    st.markdown("### 1. Selecione os filtros desejados")

    # EXIBE OS FILTROS DINÂMICOS NA TELA DO STREAMLIT, DISTRIBUÍDOS EM 6 COLUNAS.
    # OS FILTROS SÃO DISPONIBILIZADOS DE FORMA ORGANIZADA EM COLUNAS
    dynamic_filters.display_filters(
        location="columns", num_columns=len(list_filters_selectbox)
    )

    # APLICA OS FILTROS SELECIONADOS PELO USUÁRIO AO DATAFRAME ORIGINAL
    df_filtered = dynamic_filters.filter_df()

    # ARMAZENA UMA CÓPIA DO DATAFRAME FILTRADO PARA EXIBIÇÃO VISUAL FUTURA (df_viz).
    df_viz = df_filtered

    # SELECIONA APENAS AS COLUNAS "AGENCIA" E "STATUS CONSOLIDADO" DO DATAFRAME FILTRADO
    df_filtered = df_filtered[["AGENCIA", "STATUS CONSOLIDADO"]]

    # AGRUPA O DATAFRAME PELA COLUNA "STATUS CONSOLIDADO" E CONTA O NÚMERO DE AGÊNCIAS POR STATUS.
    df_aux = (
        df_filtered.groupby(["STATUS CONSOLIDADO"])
        .count()  # CONTA O NÚMERO DE AGÊNCIAS PARA CADA STATUS CONSOLIDADO
        .reset_index()  # REINICIA O ÍNDICE PARA UMA MELHOR ORGANIZAÇÃO
        .sort_values(
            by="AGENCIA",
            ascending=False,  # ORDENA PELO NÚMERO DE AGÊNCIAS EM ORDEM DECRESCENTE
        )
    )

    # SUBSTITUI O VALOR "0" NA COLUNA "STATUS CONSOLIDADO" POR "OUTRO", CASO EXISTA
    df_aux["STATUS CONSOLIDADO"] = df_aux["STATUS CONSOLIDADO"].replace("0", "OUTRO")

    # CALCULA O TOTAL DE AGÊNCIAS FILTRADAS QUE ESTÃO NA ESTEIRA (OU SEJA, CUJA COLUNA "ESTEIRA" NÃO ESTÁ VAZIA)
    cont = df_viz.loc[df_viz["ESTEIRA"] != "-"]
    x = int(len(cont))  # O TOTAL É ARMAZENADO NA VARIÁVEL `x`

    # CRIA UMA LISTA DE DATAS PARA SEREM EXIBIDAS NO GRÁFICO WATERFALL (EM CASCATAS)
    dates = ["Total de Agências", "Agências em Esteira"] + list(
        df_aux["STATUS CONSOLIDADO"].unique()
    )

    # CRIA UMA LISTA DE DADOS DE RECEITA (income_data) PARA O GRÁFICO
    # O PRIMEIRO ITEM É O NÚMERO TOTAL DE AGÊNCIAS, OS DEMAIS SÃO VALORES VAZIOS (SINALIZADOS POR "-")
    income_data = [int(df_viz["CD_PONTO"].nunique())] + [
        "-" for _ in range(len(list(df_aux["STATUS CONSOLIDADO"].unique())) + 1)
    ]

    # CRIA UMA LISTA DE DADOS DE DESPESA (expense_data) PARA O GRÁFICO
    # O PRIMEIRO VALOR É UM VALOR VAZIO ("-"), O SEGUNDO É O TOTAL DE AGÊNCIAS NA ESTEIRA, E OS DEMAIS SÃO OS DADOS DE AGÊNCIAS POR STATUS
    expense_data = ["-", x] + [int(i) for i in list(df_aux["AGENCIA"].unique())]

    # CRIA UMA LISTA AUXILIAR PARA ARMAZENAR O ACÚMULO DE DADOS NO GRÁFICO (PARA EXIBIÇÃO NO WATERFALL)
    aux = []
    for i in list(df_aux["AGENCIA"].unique()):  # PARA CADA AGÊNCIA
        x -= i  # SUBTRAI O VALOR DA VARIÁVEL `x`
        aux.append(int(x))  # ARMAZENA O VALOR ATUALIZADO NA LISTA AUXILIAR

    # CRIA OS DADOS AUXILIARES PARA O GRÁFICO WATERFALL
    auxiliary_data = ["-", "-"] + aux

    # EXIBE UM SUBTÍTULO PARA A SEÇÃO DE RESUMO DAS ESTEIRAS
    st.markdown("### 2. Visualize o resumo das Esteiras do Parque")

    # CRIA O GRÁFICO WATERFALL COM AS LISTAS DE DADOS CRIADAS ANTERIORMENTE
    create_waterfall_chart(dates, auxiliary_data, income_data, expense_data)

    # EXIBE UM SUBTÍTULO PARA A SEÇÃO DE DETALHAMENTO DAS ESTEIRAS
    st.markdown("### 3. Veja a Base com detalhamento das Esteiras")

    # CRIA UM CAMPO MULTI-SELEÇÃO PARA QUE O USUÁRIO SELECIONE AGÊNCIAS ESPECÍFICAS PARA VISUALIZAÇÃO
    agencia_selected = st.multiselect(
        "Selecione a Agência que deseja visualizar",
        options=df_viz[
            "AGENCIA"
        ].unique(),  # OPÇÕES SÃO AS AGÊNCIAS ÚNICAS DO DATAFRAME FILTRADO
        max_selections=1,  # PERMITE A SELEÇÃO DE NO MÁXIMO UMA AGÊNCIA
        placeholder="Selecione uma Agência",  # MENSAGEM DE ORIENTAÇÃO NO CAMPO
    )

    # FILTRA O DATAFRAME PARA EXIBIR APENAS AS COLUNAS ORIGINAIS DE df2
    df_viz = df_viz[df2.columns]

    # SE UMA AGÊNCIA FOR SELECIONADA, FILTRA O DATAFRAME PARA EXIBIR APENAS OS DADOS DESSA AGÊNCIA
    if agencia_selected:
        df_viz = df_viz.loc[df_viz["AGENCIA"].isin(agencia_selected)]

    # EXIBE O DATAFRAME FILTRADO NA TELA EM UM FORMATO EDITÁVEL (MAS NESTE CASO DESABILITADO, OU SEJA, NÃO PODE SER EDITADO PELO USUÁRIO)
    st.data_editor(df_viz, hide_index=True, use_container_width=True, disabled=True)

    # EXIBE UM SUBTÍTULO PARA A SEÇÃO "BASE 360"
    st.markdown("### 3. Visualize a Base 360")

    # CRIA UM EXPANDER, QUE OCULTA OU EXIBE O CONTEÚDO DA BASE 360 QUANDO CLICADO
    with st.expander("BASE 360"):
        # UTILIZA O `dataframe_explorer` PARA EXPLORAR O DATAFRAME `df1` INTERATIVAMENTE
        df = dataframe_explorer(df1)

        # EXIBE O DATAFRAME EXPLORADO NA TELA
        st.data_editor(df, hide_index=True, use_container_width=True, disabled=True)


main_page_esteira_agencias({})
