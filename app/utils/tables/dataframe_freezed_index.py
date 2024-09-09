import streamlit as st
import pandas as pd
import numpy as np


# df = pd.read_excel("time_series_farol.xlsx")
# for i in range(10):
#     df[f"columns_{i}"] = 8343

# df = df.set_index(["Farol", "Data"])
# df = df.style.set_sticky(axis=0)
# e = st.dataframe(df)


df = pd.DataFrame(data=[[1, 2, 3], [4, 5, 6]], columns=["A", "B", "C"])
classes = pd.DataFrame(
    [["min-val red", "", "blue"], ["red", None, "blue max-val"]],
    index=df.index,
    columns=df.columns,
)
df = pd.DataFrame(
    [[1, 2], [3, 4]],
    index=["a", "b"],
    columns=[["level0", "level0"], ["level1a", "level1b"]],
)
classes = pd.DataFrame(["min-val"], index=["a"], columns=[["level0"], ["level1a"]])
df.style.set_td_classes(classes).to_html()
print(1)

# st.dataframe(df)
########################################################################

# https://docs.reportlab.com/demos/hello_world/hello_world/

# from reportlab.pdfgen import canvas

# c = canvas.Canvas("rl-hello_again.pdf", pagesize=(595.27, 841.89))

# c.drawString(x=50, y=780, text="Hello Again")
# c.showPage()
# c.save()
