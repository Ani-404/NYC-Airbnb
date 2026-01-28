# app.py
import streamlit as st
import pandas as pd

st.set_page_config(page_title="NYC Airbnb Test App", layout="centered")

st.title("NYC Airbnb — Test Page")
st.write("If you can see this, Streamlit is working ✅")

st.divider()

# Try loading dataset
DATA_PATH = "data/AB_NYC_2019.csv"

try:
    df = pd.read_csv(DATA_PATH)
    st.success("Dataset loaded successfully 🎉")
    st.write(f"Shape of dataset: {df.shape[0]} rows × {df.shape[1]} columns")

    st.subheader("Preview of data")
    st.dataframe(df.head(10))

except Exception as e:
    st.error("Dataset could not be loaded ❌")
    st.code(str(e))
