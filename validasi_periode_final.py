
import pandas as pd

folder = r"D:\CERT_Insider_Threat"

logon = pd.read_csv(folder + r"\logon.csv")
device = pd.read_csv(folder + r"\device.csv")
insiders = pd.read_csv(folder + r"\insiders.csv")

# Gunakan CERT 4.2
insiders = insiders[
    insiders["dataset"].astype(str) == "4.2"
].copy()

# Parsing tanggal secara eksplisit
for df in [logon, device]:
    df["date"] = pd.to_datetime(
        df["date"],
        format="%m/%d/%Y %H:%M:%S",
        errors="coerce"
    )

for col in ["start", "end"]:
    insiders[col] = pd.to_datetime(
        insiders[col],
        format="%m/%d/%Y %H:%M:%S",
        errors="coerce"
    )

# Gabungkan aktivitas
activities = pd.concat([
    logon[["user", "date"]],
    device[["user", "date"]]
], ignore_index=True)

# Validasi aktivitas dalam periode insiden
hasil = []

for _, row in insiders.iterrows():
    aktivitas_user = activities[
        (activities["user"] == row["user"]) &
        (activities["date"] >= row["start"]) &
        (activities["date"] <= row["end"])
    ]

    hasil.append({
        "user": row["user"],
        "start": row["start"],
        "end": row["end"],
        "jumlah_aktivitas": len(aktivitas_user),
        "memiliki_aktivitas": len(aktivitas_user) > 0
    })

hasil_df = pd.DataFrame(hasil)

print("Total insider:", len(hasil_df))
print("Memiliki aktivitas:",
      hasil_df["memiliki_aktivitas"].sum())
print("Tidak memiliki aktivitas:",
      (~hasil_df["memiliki_aktivitas"]).sum())

print("\nContoh hasil:")
print(hasil_df.head(10))

hasil_df.to_csv(
    "hasil_validasi_periode_final.csv",
    index=False
)

print("\nFile hasil_validasi_periode_final.csv berhasil dibuat.")
