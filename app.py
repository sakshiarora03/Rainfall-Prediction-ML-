import streamlit as st
import pandas as pd

st.set_page_config(page_title="Rainfall Prediction Dashboard")

st.title("Rainfall Prediction Dashboard")

# Load cleaned dataset
df = pd.read_csv("clean_rainfall.csv")

subdivision = st.selectbox("Select Region", df["SUBDIVISION"].unique())

filtered = df[df["SUBDIVISION"] == subdivision]

st.subheader("Filtered Data")
st.dataframe(filtered)

st.subheader("Rainfall Trend")
st.line_chart(filtered.iloc[:, 2:])


if df.shape[1] > 1:
    st.line_chart(df.iloc[:, 1])

st.write("Built by Sakshi Arora")
