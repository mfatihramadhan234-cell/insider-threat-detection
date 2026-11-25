
import sqlite3

DATABASE = "database.db"

conn = sqlite3.connect(DATABASE)
conn.execute("PRAGMA foreign_keys = ON")
cursor = conn.cursor()

print("=== 1. INTEGRITAS DATABASE ===")
cursor.execute("PRAGMA integrity_check")
print(cursor.fetchone()[0])

print("\n=== 2. PEMERIKSAAN FOREIGN KEY ===")
cursor.execute("PRAGMA foreign_key_check")
hasil_fk = cursor.fetchall()

if hasil_fk:
    print("Ditemukan masalah:", hasil_fk)
else:
    print("Tidak ditemukan masalah foreign key.")

print("\n=== 3. JUMLAH DATA SETIAP TABEL ===")

tabel_list = [
    "warga",
    "logon_events",
    "device_events",
    "activity_features",
    "labeled_features",
    "model_runs",
    "detection_results"
]

for tabel in tabel_list:
    cursor.execute(f"SELECT COUNT(*) FROM {tabel}")
    print(f"{tabel}: {cursor.fetchone()[0]}")

print("\n=== 4. PEMERIKSAAN UNIQUE SOURCE ID ===")

for tabel in ["logon_events", "device_events"]:
    cursor.execute(f"""
        SELECT
            COUNT(*) - COUNT(DISTINCT source_id)
        FROM {tabel}
    """)

    print(f"{tabel}: {cursor.fetchone()[0]} duplikasi")

conn.close()
