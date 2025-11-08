import streamlit as st
import pandas as pd
import io

# Page configuration
st.set_page_config(page_title="Data Cleaning Application", page_icon="🧹", layout="wide")

st.title("🧹 Data Cleaning Application")
st.markdown("Upload your CSV or Excel file and clean your data easily!")

# File uploader
uploaded_file = st.file_uploader("📂 Upload CSV or Excel file", type=["csv", "xlsx"])

def to_excel(df):
    """Convert DataFrame to Excel bytes for download."""
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Sheet1')
        writer.save()
    processed_data = output.getvalue()
    return processed_data

if uploaded_file is not None:
    # Load file
    if uploaded_file.name.endswith('.csv'):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    # Display basic info
    st.subheader("📊 Basic Summary")
    buffer = io.StringIO()
    df.info(buf=buffer)
    s = buffer.getvalue()
    st.text(s)

    st.write("Number of missing values per column:")
    st.write(df.isnull().sum())

    st.write("Number of duplicate records:")
    st.write(df.duplicated().sum())

    st.subheader("⚡ Data Cleaning Options")

    # Remove missing values
    if st.button("Remove missing values"):
        cleaned_df = df.dropna()
        st.success("✅ Missing values removed!")
        st.download_button(
            label="Download Cleaned File",
            data=to_excel(cleaned_df),
            file_name="cleaned_data.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

    # Handle missing values
    if st.button("Handle missing values (fillna for objects, interpolate for numerical)"):
        cleaned_df = df.copy()
        for col in cleaned_df.columns:
            if cleaned_df[col].dtype == 'object':
                cleaned_df[col].fillna('Unknown', inplace=True)
            else:
                cleaned_df[col] = cleaned_df[col].interpolate()
        st.success("✅ Missing values handled!")
        st.download_button(
            label="Download Cleaned File",
            data=to_excel(cleaned_df),
            file_name="filled_data.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

    # Remove duplicate values
    if st.button("Remove duplicate values"):
        cleaned_df = df.drop_duplicates()
        st.success("✅ Duplicate records removed!")
        st.download_button(
            label="Download Cleaned File",
            data=to_excel(cleaned_df),
            file_name="deduplicated_data.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
