import streamlit as st
import kagglehub
import pandas as pd
import os

st.title("Age at Death Predictor")

try:
    # Download dataset
    st.write("Downloading dataset...")

    path = kagglehub.dataset_download("imoore/age-dataset")

    st.success(f"Dataset downloaded: {path}")

    # Show files
    files = os.listdir(path)

    st.write("Files found:")
    st.write(files)

    # Find CSV
    csv_files = [
        file for file in files
        if file.lower().endswith(".csv")
    ]

    if not csv_files:
        st.error("No CSV file found.")
        st.stop()

    csv_path = os.path.join(path, csv_files[0])

    # Read CSV
    df = pd.read_csv(csv_path)

    st.success("Dataset loaded successfully!")

    # Show information
    st.write("Shape:", df.shape)

    st.write("Columns:")
    st.write(df.columns.tolist())

    st.subheader("First 10 rows")

    st.dataframe(df.head(10))

except Exception as e:

    st.error("Something went wrong:")

    st.exception(e)
