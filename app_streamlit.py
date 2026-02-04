import streamlit as st
import pandas as pd
import joblib
import matplotlib.pyplot as plt

# ================= CONFIG =================
st.set_page_config(page_title="Rainfall Dashboard", layout="wide")

MONTHS = ["JAN","FEB","MAR","APR","MAY","JUN",
          "JUL","AUG","SEP","OCT","NOV","DEC"]

# ================= LOAD DATA =================
df = pd.read_csv("clean_rainfall.csv")
model = joblib.load("best_rainfall_model.pkl")
model_cmp = pd.read_csv("model_comparison_results.csv")


subdivisions = sorted(df["SUBDIVISION"].unique())

months = {
    "January": "JAN",
    "February": "FEB",
    "March": "MAR",
    "April": "APR",
    "May": "MAY",
    "June": "JUN",
    "July": "JUL",
    "August": "AUG",
    "September": "SEP",
    "October": "OCT",
    "November": "NOV",
    "December": "DEC"
}

# ================= SIDEBAR =================
page = st.sidebar.radio(
    "Navigation",
    ["🏠 Overview", "🔮 Prediction", "📊 Analytics"]
)

# ==================================================
# 🏠 OVERVIEW PAGE (UNCHANGED UI)
# ==================================================
if page == "🏠 Overview":
    st.title("🌧️ Rainfall Prediction Dashboard")

    st.markdown("""
    ### 📌 Project Overview
    This project predicts **annual rainfall** using historical rainfall data
    collected from Indian subdivisions.

    ### 📊 Dataset
    - Indian Rainfall Dataset (1901–2015)
    - Cleaned and preprocessed
    - Monthly rainfall used as features

    ### 🤖 Machine Learning Models (5)
    - Linear Regression  
    - Ridge Regression  
    - Lasso Regression  
    - Decision Tree  
    - Random Forest  

    ### 🏆 Best Model
    - Selected using **MSE & R² Score**
    """)

# ==================================================
# 🔮 PREDICTION PAGE (DROPDOWN BASED – FINAL)
# ==================================================
elif page == "🔮 Prediction":
    st.title("🔮 Rainfall Prediction")

    col1, col2 = st.columns(2)

    with col1:
        subdivision = st.selectbox("Select Subdivision", subdivisions)
        month_name = st.selectbox("Select Month", list(months.keys()))

    with col2:
        st.markdown("### 📤 Prediction Output")

    if st.button("Predict Rainfall"):
        row = df[df["SUBDIVISION"] == subdivision].iloc[-1]

        monthly_values = row[MONTHS]
        input_data = pd.DataFrame([monthly_values], columns=MONTHS)

        prediction = model.predict(input_data)[0]

        category = (
            "Heavy Rain" if prediction > df["ANNUAL"].quantile(0.75)
            else "Normal Rain"
        )

        st.success(f"🌧️ **Predicted Annual Rainfall:** {prediction:.2f} mm")
        st.info(f"☁️ **Rainfall Category:** {category}")

# ==================================================
# 📊 ANALYTICS PAGE (ALL VISUALS)
# ==================================================
elif page == "📊 Analytics":
    st.title("📊 Rainfall Analytics Dashboard")

    # ---------- Monthly Trend ----------
    st.subheader("📈 Average Monthly Rainfall")
    st.line_chart(df[MONTHS].mean())

    # ---------- Annual Distribution ----------
    st.subheader("📊 Annual Rainfall Distribution")
    fig, ax = plt.subplots()
    ax.hist(df["ANNUAL"], bins=30)
    ax.set_xlabel("Annual Rainfall (mm)")
    ax.set_ylabel("Frequency")
    st.pyplot(fig)

    # ---------- Monthly Boxplot ----------
    st.subheader("📦 Monthly Rainfall Spread")
    fig, ax = plt.subplots(figsize=(10,4))
    df[MONTHS].boxplot(ax=ax)
    ax.set_ylabel("Rainfall (mm)")
    plt.xticks(rotation=45)
    st.pyplot(fig)

    # ---------- Correlation Heatmap ----------
    st.subheader("🔗 Correlation Matrix")
    corr = df[MONTHS + ["ANNUAL"]].corr()
    fig, ax = plt.subplots(figsize=(10,6))
    im = ax.imshow(corr, cmap="coolwarm")
    ax.set_xticks(range(len(corr.columns)))
    ax.set_yticks(range(len(corr.columns)))
    ax.set_xticklabels(corr.columns, rotation=45, ha="right")
    ax.set_yticklabels(corr.columns)
    fig.colorbar(im)
    st.pyplot(fig)

    # ---------- Model Comparison ----------
    st.subheader("🤖 Model Comparison")

    r2_col = [c for c in model_cmp.columns if "R2" in c.upper()][0]
    mse_col = [c for c in model_cmp.columns if "MSE" in c.upper()][0]

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### R² Score Comparison")
        fig, ax = plt.subplots()
        ax.bar(model_cmp["Model"], model_cmp[r2_col])
        ax.set_ylabel("R² Score")
        plt.xticks(rotation=30)
        st.pyplot(fig)

    with col2:
        st.markdown("### MSE Comparison")
        fig, ax = plt.subplots()
        ax.bar(model_cmp["Model"], model_cmp[mse_col])
        ax.set_ylabel("Mean Squared Error")
        plt.xticks(rotation=30)
        st.pyplot(fig)
