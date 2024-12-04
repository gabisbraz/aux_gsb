from datetime import datetime

import pandas as pd
import streamlit_echarts as st_echarts

df = pd.read_excel("app/data/time_series_farol.xlsx")


def criar_grafico_echarts(
    df: pd.DataFrame,
    data_column: str,
    line_name_column: str,
    value_column: str,
    score_farol_map: dict,
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
    for farol, color in score_farol_map.items():
        # FILTRA OS DADOS DO DATAFRAME PARA OBTER OS VALORES ASSOCIADOS AO FAROL ATUAL.
        serie_data = df[df[line_name_column] == farol][value_column].tolist()

        # CRIA NOVA SÉRIE DO GRÁFICO
        series.append(
            {
                "name": farol,  # DEFINE O NOME DA SÉRIE PARA EXIBIÇÃO NA LEGENDA
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
            "data": [farol_name for farol_name in score_farol_map.keys()]
        },  # DEFINE OS NOMES DAS SÉRIES NA LEGENDA
        "grid": {
            "left": "3%",
            "right": "4%",
            "bottom": "3%",
            "containLabel": True,
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

    st_echarts.st_echarts(options=option)


criar_grafico_echarts(
    df=df,
    data_column="Data",
    line_name_column="Farol",
    value_column="Valor",
    score_farol_map={"farol_1": "red", "farol_2": "green", "farol_3": "yellow"},
)
