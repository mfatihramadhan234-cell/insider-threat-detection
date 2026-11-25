
import pandas as pd
import os

# Lokasi dataset CERT
folder = r"D:\CERT_Insider_Threat"

# Membaca dataset
print("Membaca dataset...")

logon = pd.read_csv(os.path.join(folder, "logon.csv"))
device = pd.read_csv(os.path.join(folder, "device.csv"))
insiders = pd.read_csv(os.path.join(folder, "insiders.csv"))

# Mengambil insider dari dataset versi 4.2
insiders_42 = insiders[
    pd.to_numeric(insiders["dataset"], errors="coerce") == 4.2
].copy()

# Konversi tanggal aktivitas
logon["date"] = pd.to_datetime(
    logon["date"], errors="coerce"
)

device["date"] = pd.to_datetime(
    device["date"], errors="coerce"
)

# Konversi tanggal periode insider
insiders_42["start"] = pd.to_datetime(
    insiders_42["start"], errors="coerce"
)

insiders_42["end"] = pd.to_datetime(
    insiders_42["end"], errors="coerce"
)

# Menggabungkan aktivitas logon dan device
activity = pd.concat([
    logon[["user", "date"]],
    device[["user", "date"]]
], ignore_index=True)

# Mengurutkan dan memeriksa aktivitas setiap insider
hasil = []

for _, insider in insiders_42.iterrows():

    user = insider["user"]
    start = insider["start"]
    end = insider["end"]

    aktivitas_user = activity[
        (activity["user"] == user) &
        (activity["date"] >= start) &
        (activity["date"] <= end)
    ]

    hasil.append({
        "user": user,
        "start": start,
        "end": end,
        "jumlah_aktivitas": len(aktivitas_user),
        "ada_aktivitas": len(aktivitas_user) > 0
    })

# Membuat tabel hasil
hasil_df = pd.DataFrame(hasil)

print("\n================================")
print("HASIL VALIDASI INSIDER DATASET 4.2")
print("================================")

print("\nTotal insider:", len(hasil_df))

print(
    "Memiliki aktivitas:",
    hasil_df["ada_aktivitas"].sum()
)

print(
    "Tidak memiliki aktivitas:",
    (~hasil_df["ada_aktivitas"]).sum()
)

print("\nDetail hasil:")
print(hasil_df.to_string(index=False))

# Menyimpan hasil
hasil_df.to_csv(
    "hasil_validasi_periode.csv",
    index=False
)

print("\nHasil disimpan ke hasil_validasi_periode.csv")
