import streamlit as st
import pandas as pd

st.set_page_config(page_title="Rainfall Analytics Dashboard", layout="wide")

st.title("🌧 Rainfall Analytics Dashboard")

df = pd.read_csv("clean_rainfall.csv")

# Sidebar filters
st.sidebar.header("Filters")

region = st.sidebar.selectbox("Select Region", df["SUBDIVISION"].unique())
year = st.sidebar.selectbox("Select Year", sorted(df["YEAR"].unique()))

filtered = df[(df["SUBDIVISION"] == region) & (df["YEAR"] == year)]

# KPIs
col1, col2, col3 = st.columns(3)

avg_rain = round(filtered.iloc[:, 2:].mean(axis=1).values[0], 2)
max_rain = round(filtered.iloc[:, 2:].max(axis=1).values[0], 2)
min_rain = round(filtered.iloc[:, 2:].min(axis=1).values[0], 2)

col1.metric("Average Rainfall", avg_rain)
col2.metric("Maximum Rainfall", max_rain)
col3.metric("Minimum Rainfall", min_rain)

st.divider()

st.subheader("Monthly Rainfall Trend")

months = filtered.columns[2:]
values = filtered.iloc[0, 2:]

chart_df = pd.DataFrame({"Month": months, "Rainfall": values})
st.line_chart(chart_df.set_index("Month"))

st.subheader("Filtered Dataset")
st.dataframe(filtered)

st.caption("Built by Sakshi Arora")
