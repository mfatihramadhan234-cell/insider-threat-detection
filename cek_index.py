import sqlite3

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

tabel_list = [
    "logon_events",
    "device_events",
    "activity_features",
    "labeled_features",
    "detection_results"
]

for tabel in tabel_list:
    print(f"\n=== INDEX {tabel.upper()} ===")

    cursor.execute(f"PRAGMA index_list({tabel})")

    for index in cursor.fetchall():
        print(index)

conn.close()