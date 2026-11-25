import sqlite3

DB_NAME = "database.db"

conn = sqlite3.connect(DB_NAME)
cursor = conn.cursor()

tables = [
    "warga",
    "logon_events",
    "device_events",
    "activity_features",
    "model_runs",
    "detection_results",
    "labeled_features"
]

for table in tables:
    print(f"\n{'=' * 50}")
    print(f"TABEL: {table}")
    print("=" * 50)

    cursor.execute("""
        SELECT name
        FROM sqlite_master
        WHERE type='table' AND name=?
    """, (table,))

    if not cursor.fetchone():
        print("Tabel belum tersedia.")
        continue

    cursor.execute(f"PRAGMA table_info({table})")
    for column in cursor.fetchall():
        print(column)

    cursor.execute(f"SELECT COUNT(*) FROM {table}")
    print("Jumlah data:", cursor.fetchone()[0])

    cursor.execute(f"PRAGMA foreign_key_list({table})")
    foreign_keys = cursor.fetchall()

    print("Relasi foreign key:")
    if foreign_keys:
        for fk in foreign_keys:
            print(fk)
    else:
        print("Belum ada foreign key.")

conn.close()