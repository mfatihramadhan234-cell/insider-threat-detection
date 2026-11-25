
import pandas as pd

folder = r"D:\CERT_Insider_Threat"

df = pd.read_csv(folder + r"\insiders.csv")
df = df[df["dataset"].astype(str) == "4.2"].copy()

print("Total insider CERT 4.2:", len(df))
print("\nContoh tanggal asli:")
print(df[["user", "start", "end"]].head())

for kolom in ["start", "end"]:
    df[kolom + "_parsed"] = pd.to_datetime(
        df[kolom],
        format="%m/%d/%Y %H:%M:%S",
        errors="coerce"
    )

    print(f"\nKolom: {kolom}")
    print("Tanggal gagal dibaca:", df[kolom + "_parsed"].isna().sum())
    print("Tanggal paling awal:", df[kolom + "_parsed"].min())
    print("Tanggal paling akhir:", df[kolom + "_parsed"].max())
