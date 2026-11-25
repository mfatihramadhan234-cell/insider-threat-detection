
import sqlite3
import pandas as pd
from pathlib import Path

FOLDER_DATASET = Path(r"D:\CERT_Insider_Threat")
DATABASE = "database.db"

def import_logon(conn):
    file = FOLDER_DATASET / "logon.csv"
    df = pd.read_csv(file)

    df["date"] = pd.to_datetime(
        df["date"],
        format="%m/%d/%Y %H:%M:%S",
        errors="raise"
    )

    df = df.rename(columns={
        "id": "source_id",
        "date": "event_date",
        "user": "user_id"
    })

    df = df[[
        "source_id", "event_date", "user_id", "pc", "activity"
    ]]

    df["event_date"] = df["event_date"].dt.strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    df.to_sql(
        "logon_events",
        conn,
        if_exists="append",
        index=False
    )

    print("Logon berhasil diimpor:", len(df))


def import_device(conn):
    file = FOLDER_DATASET / "device.csv"
    df = pd.read_csv(file)

    df["date"] = pd.to_datetime(
        df["date"],
        format="%m/%d/%Y %H:%M:%S",
        errors="raise"
    )

    df = df.rename(columns={
        "id": "source_id",
        "date": "event_date",
        "user": "user_id"
    })

    df = df[[
        "source_id", "event_date", "user_id", "pc", "activity"
    ]]

    df["event_date"] = df["event_date"].dt.strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    df.to_sql(
        "device_events",
        conn,
        if_exists="append",
        index=False
    )

    print("Device berhasil diimpor:", len(df))


if __name__ == "__main__":
    conn = sqlite3.connect(DATABASE)

    try:
        # Tambahkan kolom ID sumber untuk identifikasi data CERT
        conn.execute("""
            ALTER TABLE logon_events
            ADD COLUMN source_id TEXT
        """)
        conn.execute("""
            CREATE UNIQUE INDEX IF NOT EXISTS
            idx_logon_source ON logon_events(source_id)
        """)
        conn.execute("""
            ALTER TABLE device_events
            ADD COLUMN source_id TEXT
        """)
        conn.execute("""
            CREATE UNIQUE INDEX IF NOT EXISTS
            idx_device_source ON device_events(source_id)
        """)
        conn.commit()

        import_logon(conn)
        import_device(conn)
        conn.commit()

        print("\nImport dataset selesai!")

    except Exception as e:
        conn.rollback()
        print("Terjadi kesalahan:", e)

    finally:
        conn.close()
