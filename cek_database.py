
import sqlite3

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

for tabel in ["logon_events", "device_events"]:
    cursor.execute(f"SELECT COUNT(*) FROM {tabel}")
    jumlah = cursor.fetchone()[0]
    print(f"{tabel}: {jumlah:,} data")

conn.close()
