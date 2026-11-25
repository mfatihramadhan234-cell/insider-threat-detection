import sqlite3

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

tabel_list = ["logon_events", "device_events"]

for tabel in tabel_list:
    print(f"\n=== {tabel.upper()} ===")

    cursor.execute(f"""
        SELECT
            COUNT(*) AS total,
            COUNT(source_id) AS terisi,
            COUNT(DISTINCT source_id) AS unik
        FROM {tabel}
    """)

    total, terisi, unik = cursor.fetchone()

    print("Total data:", total)
    print("Source ID terisi:", terisi)
    print("Source ID unik:", unik)
    print("Source ID kosong:", total - terisi)

    cursor.execute(f"""
        SELECT source_id, COUNT(*)
        FROM {tabel}
        WHERE source_id IS NOT NULL
        GROUP BY source_id
        HAVING COUNT(*) > 1
        LIMIT 5
    """)

    duplikat = cursor.fetchall()

    print("Contoh source ID duplikat:", duplikat)

conn.close()