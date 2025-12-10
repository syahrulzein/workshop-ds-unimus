import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os


def load_data(path: str):
    if not os.path.exists(path):
        st.error(f"CSV not found at: {path}")
        return None
    try:
        df = pd.read_csv(path)
        return df
    except Exception as e:
        st.error(f"Error loading CSV: {e}")
        return None


def main():
    st.set_page_config(page_title="Pie Chart — Streamlit", layout="centered")
    st.title("Interactive Pie Chart")

    st.markdown("This app shows a pie chart for a selected categorical column from the dataset.")

    csv_path = "healthcare-dataset-stroke-data.csv"
    df = load_data(csv_path)
    if df is None:
        st.stop()

    # Let user pick a column to visualize
    categorical_cols = [c for c in df.columns if df[c].dtype == 'object' or df[c].nunique() <= 20]
    if not categorical_cols:
        st.warning("No suitable categorical columns found.")
        st.dataframe(df.head())
        return

    col = st.selectbox("Select categorical column for pie chart", categorical_cols)

    counts = df[col].value_counts(dropna=False)

    st.subheader(f"Distribution of `{col}`")
    st.write(counts)

    fig, ax = plt.subplots()
    ax.pie(counts, labels=counts.index.astype(str), autopct="%1.1f%%", startangle=90)
    ax.axis("equal")
    st.pyplot(fig)

    with st.expander("Show raw data"):
        st.dataframe(df)


if __name__ == "__main__":
    main()
