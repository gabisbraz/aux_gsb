from datetime import datetime

import pandas as pd
import streamlit_echarts as st_echarts
import streamlit as st

df = pd.read_excel("BASE_HISTORICA.xlsx")


def criar_grafico_echarts(
    df: pd.DataFrame,
    data_column: str,
    list_columns_values: list,
    score_farol_map: dict,
    nome_coluna_agencia: str,
    codigo_agencia: int,
):
    # CONVERTE A COLUNA PARA DATETIME
    df[data_column] = pd.to_datetime(df[data_column])

    # FORMATA A DATA NO FORMATO "MÊS/ANO"
    df["DATA_FORMATTED"] = df[data_column].dt.strftime("%b/%y")

    # EXTRAI AS DATAS FORMATADAS COMO UMA LISTA --> EIXO X
    x_axis_data = df["DATA_FORMATTED"].unique().tolist()
    x_axis_data.sort(key=lambda date: datetime.strptime(date, "%b/%y"))

    # INICIALIZA LISTA PARA CONFIGS. DAS SÉRIES
    series = []

    # ITERA SOBRE OS FARÓIS DO SCOREFAROLMAP DATACLASS.
    for col, color in score_farol_map.items():

        if col in list_columns_values:

            # FILTRA OS DADOS DO DATAFRAME PARA OBTER OS VALORES ASSOCIADOS AO FAROL ATUAL.
            serie_data = df[df[nome_coluna_agencia] == codigo_agencia][col].tolist()

            # CRIA NOVA SÉRIE DO GRÁFICO
            series.append(
                {
                    "name": col,  # DEFINE O NOME DA SÉRIE PARA EXIBIÇÃO NA LEGENDA
                    "type": "line",  # ESPECIFICA QUE A SÉRIE SERÁ UMA LINHA
                    "data": serie_data,  # ATRIBUI OS DADOS DA SÉRIE (VALORES DO FAROL)
                    "itemStyle": {"color": color},  # DEFINE A COR DA LINHA
                    "lineStyle": {
                        "width": 2,
                        "color": color,
                    },  # FORMATA A LARGURA E A COR DA LINHA
                    "label": {
                        "position": "top",
                        "color": "black",
                    },  # ADICIONA LABEL
                    "smooth": False,  # DEFINE SE A LINHA DEVE SER CURVAS OU LINEAR.
                }
            )

    # CONFIGURAÇÕES GERAIS DO GRÁFICO
    option = {
        "tooltip": {"trigger": "axis"},  # CONFIGURA O TOOLTIP --> MOUSE SOBRE O EIXO
        "legend": {
            "data": [farol_name for farol_name in score_farol_map.keys()],
            "bottom": -5,
        },  # DEFINE OS NOMES DAS SÉRIES NA LEGENDA
        "grid": {
            "left": "3%",
            "right": "4%",
            "bottom": 100,
            "containLabel": True,
            "height": "200px",
        },  # AJUSTA AS MARGENS DO GRÁFICO
        "xAxis": {
            "type": "category",  # TIPO DO EIXO X == CATEGÓRICO (DATAS)
            "data": x_axis_data,  # VALORES DO EIXO X
            "boundaryGap": True,
            "axisTick": {"alignWithLabel": True},
            "axisLabel": {"rotate": 30, "padding": [8, 4, 4, 4]},
        },
        "yAxis": {"type": "value"},  # TIPO DO EIXO Y == VALORES NUMÉRICO
        "series": series,  # ADICIONA AS SÉRIES AO GRÁFICO
    }

    st_echarts.st_echarts(options=option, height="400px")


def main():

    agencia_selected = st.selectbox(
        "Selecione uma agência",
        options=df["CD_PONTO"].unique(),
        format_func=lambda x: str(x).zfill(4),
    )

    st.write("\n")

    dict_columns = {
        "ÁGUA": {
            "CONSUMO ÁGUA": "blue",
            "CUSTO ÁGUA": "blue",
            "SCORE ÁGUA": "blue",
        },
        "ENERGIA": {
            "CONSUMO ENERGIA": "red",
            "CUSTO ENERGIA": "red",
            "SCORE ENERGIA": "red",
        },
    }

    df_filtrado = df[df["CD_PONTO"] == agencia_selected]
    linha_data_recente = df_filtrado.loc[df_filtrado["DATA"].idxmax()]

    for kpi in dict_columns.keys():
        modal_columns = st.columns(3)
        for i, col in enumerate(dict_columns[kpi]):
            with modal_columns[i]:
                st.text_input(
                    f"{col}", disabled=True, value=f"{linha_data_recente.get(col):.2f}"
                )

    st.write("\n")
    kpis_selected = st.pills(
        "SELECIONE O KPIS QUE DESEJA VISUALIZAR",
        ["ÁGUA", "ENERGIA"],
        selection_mode="multi",
        default="ÁGUA",
    )
    st.write("\n")

    score_farol_map = {}

    colunas_valores_selected = []

    for kpi in kpis_selected:
        if kpi in dict_columns.keys():
            for coluna in dict_columns[kpi].keys():
                colunas_valores_selected.append(coluna)
            score_farol_map.update(dict_columns[kpi])

    criar_grafico_echarts(
        df=df,
        data_column="DATA",
        list_columns_values=colunas_valores_selected,
        score_farol_map=score_farol_map,
        nome_coluna_agencia="CD_PONTO",
        codigo_agencia=agencia_selected,
    )


main()
