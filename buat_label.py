
import sqlite3
import pandas as pd

DATABASE = "database.db"
FOLDER = r"D:\CERT_Insider_Threat"

def buat_label():
    conn = sqlite3.connect(DATABASE)

    print("Membaca fitur aktivitas...")
    fitur = pd.read_sql_query(
        "SELECT * FROM activity_features", conn
    )

    print("Membaca data insider CERT 4.2...")
    insider = pd.read_csv(FOLDER + r"\insiders.csv")

    insider = insider[
        insider["dataset"].astype(str) == "4.2"
    ].copy()

    # Konversi tanggal secara eksplisit
    for kolom in ["start", "end"]:
        insider[kolom] = pd.to_datetime(
            insider[kolom],
            format="%m/%d/%Y %H:%M:%S",
            errors="raise"
        )

    fitur["activity_date"] = pd.to_datetime(
        fitur["activity_date"],
        format="%Y-%m-%d"
    )

    # Cocokkan pengguna dan periode insiden
    insider = insider.rename(columns={"user": "user_id"})

    hasil = fitur.merge(
        insider[["user_id", "start", "end"]],
        on="user_id",
        how="left"
    )

    # Label 1 jika tanggal masuk periode insiden
    kondisi = (
        hasil["start"].notna() &
        (hasil["activity_date"] >= hasil["start"].dt.normalize()) &
        (hasil["activity_date"] <= hasil["end"].dt.normalize())
    )

    hasil["label"] = kondisi.astype(int)

    # Simpan hasil ke tabel baru, tanpa mengubah activity_features
    hasil_simpan = hasil[[
        "user_id",
        "activity_date",
        "login_count",
        "logoff_count",
        "after_hours_login",
        "unique_pc",
        "device_connect",
        "device_disconnect",
        "label"
    ]].copy()

    hasil_simpan["activity_date"] = (
        hasil_simpan["activity_date"].dt.strftime("%Y-%m-%d")
    )

    hasil_simpan.to_sql(
        "labeled_features",
        conn,
        if_exists="replace",
        index=False
    )

    # Distribusi label
    print("\nHASIL DISTRIBUSI LABEL")
    print("Total data:", len(hasil_simpan))
    print("Label 1 (periode insiden):", int(hasil_simpan["label"].sum()))
    print("Label 0 (di luar periode insiden):", int((hasil_simpan["label"] == 0).sum()))

    print("\nContoh data:")
    print(hasil_simpan.head(10).to_string(index=False))

    conn.close()
    print("\nLabel berhasil dibuat dalam tabel labeled_features.")

if __name__ == "__main__":
    buat_label()
