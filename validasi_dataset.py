
import pandas as pd

folder = r"D:\CERT_Insider_Threat"

logon = pd.read_csv(folder + r"\logon.csv")
device = pd.read_csv(folder + r"\device.csv")
insiders = pd.read_csv(folder + r"\insiders.csv")

# Menghitung jumlah pengguna
users_logon = set(logon["user"].dropna().unique())
users_device = set(device["user"].dropna().unique())
users_insider = set(insiders["user"].dropna().unique())

print("=== JUMLAH DATA ===")
print("Logon:", len(logon))
print("Device:", len(device))
print("Insiders:", len(insiders))

print("\n=== JUMLAH PENGGUNA ===")
print("Pengguna Logon:", len(users_logon))
print("Pengguna Device:", len(users_device))
print("Pengguna Insiders:", len(users_insider))

print("\n=== KESESUAIAN PENGGUNA ===")
print("Insider yang ada di Logon:",
      len(users_insider & users_logon))
print("Insider yang ada di Device:",
      len(users_insider & users_device))

print("\n=== JENIS AKTIVITAS ===")
print(logon["activity"].value_counts())
print(device["activity"].value_counts())

print("\n=== VERSI DATASET INSIDERS ===")
print(insiders["dataset"].value_counts())
