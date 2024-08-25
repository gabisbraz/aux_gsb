from math import ceil
from datetime import datetime

import numpy as np
import pandas as pd
import streamlit_echarts as st_echarts

from typing import List
from dataclasses import dataclass


@dataclass
class Farol:
    nome_etl: str
    nome_front: str
    cor: str
    cor_fonte: str
    icones: str
    cor_icone: str
    valor_min: float
    valor_max: float


@dataclass
class ScoreFarolMap:
    farol_list: List[Farol]


df = pd.read_excel("app/data/time_series_farol.xlsx")

farol_1 = Farol(
    nome_etl="farol_1",
    nome_front="Farol 1",
    cor="#FF5733",
    cor_fonte="#000000",
    icones="icon1",
    cor_icone="#FF5733",
    valor_min=0,
    valor_max=150,
)

farol_2 = Farol(
    nome_etl="farol_2",
    nome_front="Farol 2",
    cor="#33FF57",
    cor_fonte="#000000",
    icones="icon2",
    cor_icone="#33FF57",
    valor_min=151,
    valor_max=250,
)

farol_3 = Farol(
    nome_etl="farol_3",
    nome_front="Farol 3",
    cor="#3357FF",
    cor_fonte="#000000",
    icones="icon3",
    cor_icone="#3357FF",
    valor_min=251,
    valor_max=350,
)

score_farol_map = ScoreFarolMap(farol_list=[farol_1, farol_2, farol_3])


def criar_grafico_echarts(
    df: pd.DataFrame,
    data_column: str,
    line_name_column: str,
    value_column: str,
    score_farol_map: ScoreFarolMap,
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
    for farol in score_farol_map.farol_list:
        # FILTRA OS DADOS DO DATAFRAME PARA OBTER OS VALORES ASSOCIADOS AO FAROL ATUAL.
        serie_data = df[df[line_name_column] == farol.nome_etl][value_column].tolist()

        # CRIA NOVA SÉRIE DO GRÁFICO
        series.append(
            {
                "name": farol.nome_front,  # DEFINE O NOME DA SÉRIE PARA EXIBIÇÃO NA LEGENDA
                "type": "line",  # ESPECIFICA QUE A SÉRIE SERÁ UMA LINHA
                "data": serie_data,  # ATRIBUI OS DADOS DA SÉRIE (VALORES DO FAROL)
                "itemStyle": {"color": farol.cor},  # DEFINE A COR DA LINHA
                "lineStyle": {
                    "width": 2,
                    "color": farol.cor,
                },  # FORMATA A LARGURA E A COR DA LINHA
                "label": {
                    # "show": True,
                    "position": "top",
                    "color": farol.cor_fonte,
                },  # ADICIONA LABEL
                "smooth": False,  # DEFINE SE A LINHA DEVE SER CURVAS OU LINEAR.
            }
        )

    # CONFIGURAÇÕES GERAIS DO GRÁFICO
    option = {
        "tooltip": {"trigger": "axis"},  # CONFIGURA O TOOLTIP --> MOUSE SOBRE O EIXO
        "legend": {
            "data": [farol.nome_front for farol in score_farol_map.farol_list]
        },  # DEFINE OS NOMES DAS SÉRIES NA LEGENDA
        "grid": {
            "left": "3%",
            "right": "4%",
            "bottom": "3%",
            "containLabel": True,
        },  # AJUSTA AS MARGENS DO GRÁFICO
        "toolbox": {"feature": {"saveAsImage": {}}},
        "xAxis": {
            "type": "category",  # TIPO DO EIXO X == CATEGÓRICO (DATAS)
            "data": x_axis_data,  # VALORES DO EIXO X
        },
        "yAxis": {"type": "value"},  # TIPO DO EIXO Y == VALORES NUMÉRICO
        "series": series,  # ADICIONA AS SÉRIES AO GRÁFICO
        "dataZoom": [
            {
                "start": 100
                * (
                    (len(x_axis_data) - 12) / len(x_axis_data)
                ),  # ADICIONA A BARRA DE ZOOM NA PARTE INFERIOR DO GRÁFICO.
                "end": 100,  # CALCULA O FIM DO ZOOM PARA A BARRA.
            },
        ],
    }

    st_echarts.st_echarts(options=option)


criar_grafico_echarts(
    df=df,
    data_column="Data",
    line_name_column="Farol",
    value_column="Valor",
    score_farol_map=score_farol_map,
)
