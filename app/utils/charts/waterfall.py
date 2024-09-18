from streamlit_echarts import st_echarts
from pyecharts.commons.utils import JsCode


def create_waterfall_chart(dates, auxiliary_data, income_data, expense_data):
    options = {
        "title": {
            "text": "Waterfall Chart",
            "subtext": "From ExcelHome",
            "sublink": "http://e.weibo.com/1341556070/Aj1J2x5a5",
        },
        "tooltip": {
            "trigger": "axis",
            "axisPointer": {"type": "shadow"},
            "formatter": JsCode(
                "function(params){var tar;if(params[1].value!=='-'){tar=params[1]}else{tar=params[0]}return tar.name+'<br/>'+tar.seriesName+' : '+tar.value}"
            ).js_code,
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


# Example usage
dates = [f"November {i}" for i in range(1, 12)]
auxiliary_data = [0, 900, 1245, 1530, 1376, 1376, 1511, 1689, 1856, 1495, 1292]
income_data = [900, 345, 393, "-", "-", 135, 178, 286, "-", "-", "-"]
expense_data = ["-", "-", "-", 108, 154, "-", "-", "-", 119, 361, 203]

create_waterfall_chart(dates, auxiliary_data, income_data, expense_data)
