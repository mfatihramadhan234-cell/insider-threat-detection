
import pandas as pd

folder = r"D:\CERT_Insider_Threat"

files = ["logon.csv", "device.csv"]

for file in files:
    df = pd.read_csv(folder + "\\" + file)

    df["date_parsed"] = pd.to_datetime(
        df["date"],
        format="%m/%d/%Y %H:%M:%S",
        errors="coerce"
    )

    print("\nFILE:", file)
    print("Total data:", len(df))
    print("Tanggal gagal dibaca:", df["date_parsed"].isna().sum())
    print("Tanggal paling awal:", df["date_parsed"].min())
    print("Tanggal paling akhir:", df["date_parsed"].max())
