import os
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

from utils.etl import load_and_prepare

st.set_page_config(page_title="Dashboard Prediksi USD/IDR", layout="wide")
st.title("Dashboard Prediksi Kurs USD/IDR")

tab1, tab2 = st.tabs(["📊 Data & ETL", "📈 Hasil Prediksi & Metrik"])

# =========================
# TAB 1: DATA & ETL
# =========================
with tab1:
    kurs_daily, kurs_monthly, df = load_and_prepare(
        "data/kurs_harian.csv",
        "data/m2_bulanan.csv",
        "data/birate_bulanan.csv"
    )

    st.subheader("Ringkasan Data (Hasil Pengolahan)")
    c1, c2, c3 = st.columns(3)
    c1.metric("Baris kurs harian", len(kurs_daily))
    c2.metric("Baris kurs bulanan", len(kurs_monthly))
    c3.metric("Baris dataset final", len(df))

    st.write("Periode:", df["month"].min().date(), "s.d.", df["month"].max().date())
    st.dataframe(df.head(10), use_container_width=True)

    st.subheader("Visualisasi")
    col1, col2 = st.columns(2)

    with col1:
        st.write("Mid-rate Harian")
        fig = plt.figure()
        plt.plot(kurs_daily["date"], kurs_daily["mid_rate"])
        plt.xlabel("Tanggal")
        plt.ylabel("USD/IDR (mid-rate)")
        st.pyplot(fig)

    with col2:
        st.write("Kurs Bulanan (mid-rate)")
        fig = plt.figure()
        plt.plot(kurs_monthly["month"], kurs_monthly["usd_idr"])
        plt.xlabel("Bulan")
        plt.ylabel("USD/IDR (bulanan)")
        st.pyplot(fig)


# =========================
# TAB 2: HASIL PREDIKSI & METRIK
# =========================
with tab2:
    st.subheader("Cek File di Folder data/")
    st.write(os.listdir("data"))

    # ---- METRICS ----
    st.subheader("Metrik Evaluasi")
    metrics_path = "data/metrics.csv"
    if os.path.exists(metrics_path):
        metrics_df = pd.read_csv(metrics_path)
        st.dataframe(metrics_df, use_container_width=True)
    else:
        st.warning("File data/metrics.csv tidak ditemukan.")

    # ---- PREDICTIONS ----
    st.subheader("Hasil Prediksi")
    pred_path = "data/predictions.csv"
    if os.path.exists(pred_path):
        pred_df = pd.read_csv(pred_path)

        # parse tanggal kalau ada kolom date
        if "date" in pred_df.columns:
            pred_df["date"] = pd.to_datetime(pred_df["date"])

        st.dataframe(pred_df.head(30), use_container_width=True)

        # Plot aktual vs prediksi (kalau kolomnya sesuai)
        needed = {"date", "actual", "pred_arima_exog", "pred_lstm"}
        if needed.issubset(set(pred_df.columns)):
            st.write("Aktual vs Prediksi")
            fig = plt.figure()
            plt.plot(pred_df["date"], pred_df["actual"], label="Actual")
            plt.plot(pred_df["date"], pred_df["pred_arima_exog"], label="ARIMA (exog)")
            plt.plot(pred_df["date"], pred_df["pred_lstm"], label="LSTM")
            plt.legend()
            plt.xlabel("Bulan")
            plt.ylabel("USD/IDR")
            st.pyplot(fig)

            # Absolute error
            st.write("Absolute Error per Bulan")
            pred_df["err_arima"] = (pred_df["actual"] - pred_df["pred_arima_exog"]).abs()
            pred_df["err_lstm"] = (pred_df["actual"] - pred_df["pred_lstm"]).abs()
            fig = plt.figure()
            plt.plot(pred_df["date"], pred_df["err_arima"], label="|Error| ARIMA (exog)")
            plt.plot(pred_df["date"], pred_df["err_lstm"], label="|Error| LSTM")
            plt.legend()
            plt.xlabel("Bulan")
            plt.ylabel("Absolute Error")
            st.pyplot(fig)
        else:
            st.warning(f"Kolom predictions.csv belum sesuai. Kolom yang ada: {list(pred_df.columns)}")
    else:
        st.warning("File data/predictions.csv tidak ditemukan.")
