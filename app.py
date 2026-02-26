import streamlit as st
import matplotlib.pyplot as plt
from utils.etl import load_and_prepare

st.set_page_config(page_title="Dashboard Prediksi USD/IDR", layout="wide")
st.title("Dashboard Prediksi Kurs USD/IDR")

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