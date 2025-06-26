import streamlit as st
from streamlit_echarts import st_echarts

# Dados de entrada
dados = {
    "KPI": ["Atendimento", "Vendas", "Satisfação"],
    "Qtd Agências Críticas": [12, 8, 5],
    "% Agências Críticas": [40.0, 26.7, 16.7],
}

# Dados formatados
bar_data = dados["Qtd Agências Críticas"]
percent_labels = [f"{p:.1f}%" for p in dados["% Agências Críticas"]]

# Construir a lista de dados com tooltip customizado
data_with_tooltip = [
    {
        "value": bar_data[i],
        "tooltip": {
            "formatter": f"""
                <b>{dados['KPI'][i]}</b><br/>
                Qtd Agências Críticas: {bar_data[i]}<br/>
                % Agências Críticas: {percent_labels[i]}
            """
        },
        "label": {"show": True, "position": "top", "formatter": percent_labels[i]},
    }
    for i in range(len(bar_data))
]

# Opções do gráfico
options = {
    "title": {"text": "Indicadores de Agências Críticas"},
    "tooltip": {
        "trigger": "item",
        "formatter": None,  # Será usado o formatter específico por item
    },
    "xAxis": {"type": "category", "data": dados["KPI"]},
    "yAxis": {"type": "value", "name": "Qtd Agências Críticas"},
    "series": [
        {
            "type": "bar",
            "data": data_with_tooltip,
            "itemStyle": {"color": "#5470C6"},
        }
    ],
}

# Exibir gráfico
st_echarts(options=options, height="500px")
