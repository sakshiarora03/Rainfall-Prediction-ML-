import streamlit as st
import pandas as pd

st.set_page_config(page_title="Rainfall Prediction Dashboard")

st.title("Rainfall Prediction Dashboard")

# change filename if yours is different
df = pd.read_csv("rainfall.csv")

st.subheader("Dataset")
st.dataframe(df)

if "Rainfall" in df.columns:
    st.subheader("Rainfall Trend")
    st.line_chart(df["Rainfall"])

st.write("Built by Sakshi Arora")
