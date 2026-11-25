
import sqlite3
import csv
from datetime import datetime

# Lokasi database dan dataset
DB_PATH = "database.db"
CSV_PATH = r"D:\CERT_Insider_Threat\insiders.csv"

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Membuat tabel kasus insider
cursor.execute("""
CREATE TABLE IF NOT EXISTS insider_cases (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    dataset_version TEXT NOT NULL,
    scenario INTEGER NOT NULL,
    details TEXT,
    user_id TEXT NOT NULL,
    start_date TEXT NOT NULL,
    end_date TEXT NOT NULL,
    UNIQUE(dataset_version, scenario, user_id)
)
""")

# Membaca dataset dan mengambil versi 4.2
total = 0

with open(CSV_PATH, "r", newline="", encoding="utf-8-sig") as file:
    reader = csv.DictReader(file)

    for row in reader:
        if row["dataset"].strip() != "4.2":
            continue

        start_date = datetime.strptime(
            row["start"].strip(), "%m/%d/%Y %H:%M:%S"
        ).strftime("%Y-%m-%d %H:%M:%S")

        end_date = datetime.strptime(
            row["end"].strip(), "%m/%d/%Y %H:%M:%S"
        ).strftime("%Y-%m-%d %H:%M:%S")

        cursor.execute("""
            INSERT OR IGNORE INTO insider_cases
            (dataset_version, scenario, details, user_id, start_date, end_date)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            row["dataset"].strip(),
            int(row["scenario"]),
            row["details"].strip(),
            row["user"].strip(),
            start_date,
            end_date
        ))

        total += cursor.rowcount

conn.commit()

cursor.execute("SELECT COUNT(*) FROM insider_cases")
jumlah = cursor.fetchone()[0]

print("Import data insider selesai!")
print("Data baru dimasukkan:", total)
print("Total data dalam tabel:", jumlah)

conn.close()
