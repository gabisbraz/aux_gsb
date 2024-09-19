from streamlit_echarts import st_echarts
from pyecharts.commons.utils import JsCode


def create_waterfall_chart(dates, auxiliary_data, income_data, expense_data):
    options = {
        "title": {
            "text": "Waterfall Chart",
            "subtext": "From ExcelHome",
        },
        "tooltip": {
            "trigger": "axis",
            "axisPointer": {"type": "shadow"},
        },
        "legend": {"data": ["Expense", "Income"]},
        "grid": {"left": "3%", "right": "4%", "bottom": "3%", "containLabel": True},
        "xAxis": {
            "type": "category",
            "splitLine": {"show": False},
            "data": dates,
        },
        "yAxis": {"type": "value"},
        "series": [
            {
                "name": "Auxiliary",
                "type": "bar",
                "stack": "Total",
                "itemStyle": {
                    "barBorderColor": "rgba(0,0,0,0)",
                    "color": "rgba(0,0,0,0)",
                },
                "emphasis": {
                    "itemStyle": {
                        "barBorderColor": "rgba(0,0,0,0)",
                        "color": "rgba(0,0,0,0)",
                    }
                },
                "data": auxiliary_data,
            },
            {
                "name": "Income",
                "type": "bar",
                "stack": "Total",
                "label": {"show": True, "position": "top"},
                "data": income_data,
            },
            {
                "name": "Expense",
                "type": "bar",
                "stack": "Total",
                "label": {"show": True, "position": "bottom"},
                "data": expense_data,
            },
        ],
    }
    st_echarts(options=options, height="500px")


import pandas as pd


def prepare_waterfall_data(df, initial_value):
    auxiliary_data = [0] * (len(df) + 2)  # Incluímos 2 barras antes do df
    income_data = ["-"] * (len(df) + 2)  # As receitas começam vazias
    expense_data = ["-"] * (len(df) + 2)  # As despesas também começam vazias

    income_data[0] = initial_value

    if "agencia" in df.columns:
        income_data[1] = int(df["agencia"].sum())

    cumulative_sum = income_data[1]

    for i in range(2, len(df) + 2):
        expense_value = -int(df.iloc[i - 2]["agencia"])
        auxiliary_data[i] = cumulative_sum
        cumulative_sum -= expense_value
        expense_data[i] = expense_value if expense_value != 0 else "-"

    dates = ["Start", "Agency Total"] + df["status"].tolist()
    return dates, auxiliary_data, income_data, expense_data


data = {
    "status": ["Status 1", "Status 2", "Status 3", "Status 4"],  # Nomes das barras
    "agencia": [400, 300, 500, 200],  # Contagem de agências para cada status
}

df = pd.DataFrame(data)

dates, auxiliary_data, income_data, expense_data = prepare_waterfall_data(df, 900)

# Example usage
# dates = [f"November {i}" for i in range(1, 12)]
# auxiliary_data = [0, 900, 1245, 1530, 1376, 1376, 1511, 1689, 1856, 1495, 1292]
# income_data = [900, 345, 393, "-", "-", 135, 178, 286, "-", "-", "-"]
# expense_data = ["-", "-", "-", 108, 154, "-", "-", "-", 119, 361, 203]

create_waterfall_chart(dates, auxiliary_data, income_data, expense_data)
