
import sqlite3
import pandas as pd

DATABASE = "database.db"

# Jam kerja yang digunakan untuk analisis awal
JAM_MULAI = 8
JAM_SELESAI = 17


def ekstraksi_fitur():
    conn = sqlite3.connect(DATABASE)

    print("Mengambil data aktivitas...")

    # Ambil data logon dan logoff
    logon = pd.read_sql_query("""
        SELECT event_date, user_id, pc, activity
        FROM logon_events
    """, conn)

    # Ambil data koneksi perangkat
    device = pd.read_sql_query("""
        SELECT event_date, user_id, pc, activity
        FROM device_events
    """, conn)

    print("Data berhasil dibaca.")
    
    # Konversi tanggal
    logon["event_date"] = pd.to_datetime(logon["event_date"])
    device["event_date"] = pd.to_datetime(device["event_date"])

    # Ekstraksi tanggal aktivitas
    logon["activity_date"] = logon["event_date"].dt.date
    device["activity_date"] = device["event_date"].dt.date

    # Fitur login
    logon["login_count"] = (
        logon["activity"] == "Logon"
    ).astype(int)

    # Fitur logout
    logon["logoff_count"] = (
        logon["activity"] == "Logoff"
    ).astype(int)

    # Login di luar jam kerja (sebelum 08.00 atau mulai 17.00)
    logon["after_hours_login"] = (
        (logon["activity"] == "Logon") &
        (
            (logon["event_date"].dt.hour < JAM_MULAI) |
            (logon["event_date"].dt.hour >= JAM_SELESAI)
        )
    ).astype(int)

    # Hitung login, logout, dan login di luar jam kerja
    fitur_logon = logon.groupby(
        ["user_id", "activity_date"]
    ).agg(
        login_count=("login_count", "sum"),
        logoff_count=("logoff_count", "sum"),
        after_hours_login=("after_hours_login", "sum"),
        unique_pc=("pc", "nunique")
    ).reset_index()

    # Fitur aktivitas perangkat
    device["device_connect"] = (
        device["activity"] == "Connect"
    ).astype(int)

    device["device_disconnect"] = (
        device["activity"] == "Disconnect"
    ).astype(int)

    fitur_device = device.groupby(
        ["user_id", "activity_date"]
    ).agg(
        device_connect=("device_connect", "sum"),
        device_disconnect=("device_disconnect", "sum")
    ).reset_index()

    # Gabungkan fitur logon dan device
    fitur = pd.merge(
        fitur_logon,
        fitur_device,
        on=["user_id", "activity_date"],
        how="outer"
    )

    # Isi nilai kosong dengan 0
    kolom_fitur = [
        "login_count",
        "logoff_count",
        "after_hours_login",
        "unique_pc",
        "device_connect",
        "device_disconnect"
    ]

    fitur[kolom_fitur] = fitur[kolom_fitur].fillna(0)

    # Konversi tanggal ke format SQLite
    fitur["activity_date"] = (
        pd.to_datetime(fitur["activity_date"])
        .dt.strftime("%Y-%m-%d")
    )

    # Simpan ke tabel activity_features
    cursor = conn.cursor()

    cursor.execute("DELETE FROM activity_features")

    fitur.to_sql(
        "activity_features",
        conn,
        if_exists="append",
        index=False
    )

    conn.commit()

    print("\nEkstraksi fitur selesai!")
    print("Jumlah data fitur:", len(fitur))
    print("\nContoh hasil:")
    print(fitur.head(10).to_string(index=False))

    conn.close()


if __name__ == "__main__":
    ekstraksi_fitur()
