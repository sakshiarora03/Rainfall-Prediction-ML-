import streamlit as st
import pandas as pd

st.set_page_config(page_title="Rainfall Prediction Dashboard")

st.title("Rainfall Prediction Dashboard")

# Load cleaned dataset
df = pd.read_csv("clean_rainfall.csv")

st.subheader("Dataset Preview")
st.dataframe(df.head())

st.subheader("Rainfall Trend")

if df.shape[1] > 1:
    st.line_chart(df.iloc[:, 1])

st.write("Built by Sakshi Arora")
