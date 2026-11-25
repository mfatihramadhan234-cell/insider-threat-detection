
import pandas as pd
import os

folder = r"D:\CERT_Insider_Threat"

files = ["logon.csv", "device.csv", "insiders.csv"]

for file in files:
    path = os.path.join(folder, file)

    print("\n==============================")
    print("FILE:", file)
    print("==============================")

    df = pd.read_csv(path, nrows=5)

    print("Kolom:")
    print(df.columns.tolist())

    print("\nContoh data:")
    print(df.head(3).to_string(index=False))
