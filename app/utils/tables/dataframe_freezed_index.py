import streamlit as st
import pandas as pd


df = pd.read_excel("time_series_farol.xlsx")
for i in range(10):
    df[f"columns_{i}"] = 8343

df = df.set_index(["Farol", "Data"])
df = df.style.set_sticky(axis=0)
e = st.dataframe(df)

########################################################################

# https://docs.reportlab.com/demos/hello_world/hello_world/

from reportlab.pdfgen import canvas

c = canvas.Canvas("rl-hello_again.pdf", pagesize=(595.27, 841.89))

c.drawString(x=50, y=780, text="Hello Again")
c.showPage()
c.save()
