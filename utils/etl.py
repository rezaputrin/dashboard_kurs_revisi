import pandas as pd

def load_and_prepare(kurs_path, m2_path, rate_path):
    kurs = pd.read_csv(kurs_path)
    m2 = pd.read_csv(m2_path)
    rate = pd.read_csv(rate_path)

    kurs["date"] = pd.to_datetime(kurs["date"])
    kurs = kurs.sort_values("date")

    # mid-rate harian
    kurs["mid_rate"] = (kurs["buy"] + kurs["sell"]) / 2

    # jadi bulanan
    kurs_bulanan = (
        kurs.set_index("date")["mid_rate"]
        .resample("MS").mean()
        .to_frame("usd_idr")
        .reset_index()
        .rename(columns={"date": "month"})
    )

    # pastikan kolom bulan di m2 & rate sesuai (kalau beda nama, sesuaikan)
    m2["month"] = pd.to_datetime(m2["month"])
    rate["month"] = pd.to_datetime(rate["month"])

    df = (
        kurs_bulanan
        .merge(m2, on="month", how="left")
        .merge(rate, on="month", how="left")
        .dropna()
        .sort_values("month")
        .reset_index(drop=True)
    )

    return kurs, kurs_bulanan, df