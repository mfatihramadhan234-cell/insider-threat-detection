import sqlite3

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

index_list = [
    "idx_logon_source",
    "idx_logon_source_id",
    "idx_device_source",
    "idx_device_source_id"
]

for index in index_list:
    print(f"\n=== {index} ===")

    cursor.execute(f"PRAGMA index_info({index})")

    for row in cursor.fetchall():
        print(row)

conn.close()