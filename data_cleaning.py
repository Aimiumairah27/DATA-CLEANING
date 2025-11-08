import streamlit as st
import pandas as pd
import io

st.set_page_config(page_title="Data Cleaning App", page_icon="🧹", layout="wide")

st.markdown(
    """
    <style>
    body {background-color: #000000; color: #FFFFFF;}
    h1, h2, h3 {color: #FFDD00;}
    .stButton>button {background-color: #1f77b4; color: white; border-radius:5px;}
    .stDownloadButton>button {background-color: #FF6347; color: white; border-radius:5px;}
    </style>
    """, unsafe_allow_html=True
)

st.title("🧹 Data Cleaning Application")
st.markdown("Upload any dataset and clean it easily!")

uploaded_file = st.file_uploader("📂 Upload CSV or Excel file", type=["csv", "xlsx"])

def to_csv(df):
    return df.to_csv(index=False).encode('utf-8')

if uploaded_file is not None:
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    st.success(f"✅ File '{uploaded_file.name}' uploaded successfully!")

    st.subheader("📊 Dataset Overview")
    st.write(f"Rows: {df.shape[0]} | Columns: {df.shape[1]}")
    st.write(f"Total Missing Values: {df.isnull().sum().sum()}")
    st.write(f"Total Duplicate Records: {df.duplicated().sum()}")

    st.subheader("👀 Data Preview")
    st.dataframe(df.head())

    st.subheader("🧾 Info Summary")
    buffer = io.StringIO()
    df.info(buf=buffer)
    st.text(buffer.getvalue())

    st.subheader("🛠 Data Cleaning Options")

    if st.button("Click to Remove Missing Values"):
        cleaned_df = df.dropna()
        st.download_button(
            label="Download Cleaned CSV",
            data=to_csv(cleaned_df),
            file_name="cleaned_missing_removed.csv",
            mime="text/csv"
        )

    if st.button("Click to Handle Missing Values"):
        cleaned_df = df.copy()
        for col in cleaned_df.columns:
            if cleaned_df[col].dtype == "object":
                cleaned_df[col].fillna("Unknown", inplace=True)
            else:
                cleaned_df[col] = cleaned_df[col].interpolate()
        st.download_button(
            label="Download Cleaned CSV",
            data=to_csv(cleaned_df),
            file_name="cleaned_missing_handled.csv",
            mime="text/csv"
        )

    if st.button("Click to Remove Duplicate Records"):
        cleaned_df = df.drop_duplicates()
        st.download_button(
            label="Download Cleaned CSV",
            data=to_csv(cleaned_df),
            file_name="cleaned_duplicates_removed.csv",
            mime="text/csv"
        )

else:
    st.info("📁 Please upload a CSV or Excel file to start cleaning your data.")
