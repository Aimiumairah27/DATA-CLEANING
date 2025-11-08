import streamlit as st
import pandas as pd
import io

# Page configuration
st.set_page_config(page_title="Data Cleaning Application", page_icon="🧹", layout="wide")

# Heading
st.title("🧹 Data Cleaning Application")
st.markdown("Upload your CSV or Excel file and clean your data easily!")

# File uploader
uploaded_file = st.file_uploader("📂 Upload CSV or Excel file", type=["csv", "xlsx"])

# Function to convert DataFrame to CSV for download
def to_csv(df):
    return df.to_csv(index=False).encode('utf-8')

# Load dataset
if uploaded_file is not None:
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    st.subheader("📊 Basic Summary")
    buffer = io.StringIO()
    df.info(buf=buffer)
    st.text(buffer.getvalue())

    st.write("Number of missing values per column:")
    st.write(df.isnull().sum())

    st.write("Number of duplicate records:")
    st.write(df.duplicated().sum())

    st.subheader("⚡ Data Cleaning Options")

    # 1️⃣ Remove missing values
    if st.button("Remove missing values"):
        cleaned_df = df.dropna()
        st.success("✅ Missing values removed!")
        st.download_button(
            label="Download CSV",
            data=to_csv(cleaned_df),
            file_name="cleaned_missing_removed.csv",
            mime="text/csv"
        )

    # 2️⃣ Handle missing values
    if st.button("Handle missing values (fillna for objects, interpolate for numerical)"):
        cleaned_df = df.copy()
        for col in cleaned_df.columns:
            if cleaned_df[col].dtype == 'object':
                cleaned_df[col].fillna("Unknown", inplace=True)
            else:
                cleaned_df[col] = cleaned_df[col].interpolate()
        st.success("✅ Missing values handled!")
        st.download_button(
            label="Download CSV",
            data=to_csv(cleaned_df),
            file_name="cleaned_missing_filled.csv",
            mime="text/csv"
        )

    # 3️⃣ Remove duplicate values
    if st.button("Remove duplicate values"):
        cleaned_df = df.drop_duplicates()
        st.success("✅ Duplicate records removed!")
        st.download_button(
            label="Download CSV",
            data=to_csv(cleaned_df),
            file_name="cleaned_duplicates_removed.csv",
            mime="text/csv"
        )

else:
    st.info("📁 Please upload a CSV or Excel file to start cleaning your data.")