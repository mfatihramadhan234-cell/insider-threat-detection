
import sqlite3

conn = sqlite3.connect("database.db")
conn.execute("PRAGMA foreign_keys = ON")
cursor = conn.cursor()

print("=== STRUKTUR LABELED FEATURES ===")
cursor.execute("PRAGMA table_info(labeled_features)")

for row in cursor.fetchall():
    print(row)

print("\n=== FOREIGN KEY ===")
cursor.execute("PRAGMA foreign_key_list(labeled_features)")

for row in cursor.fetchall():
    print(row)

print("\n=== PEMERIKSAAN INTEGRITAS ===")
cursor.execute("PRAGMA foreign_key_check")

hasil = cursor.fetchall()

if hasil:
    print("Ditemukan masalah:", hasil)
else:
    print("Tidak ditemukan masalah foreign key.")

print("\n=== JUMLAH DATA ===")

for tabel in ["activity_features", "labeled_features"]:
    cursor.execute(f"SELECT COUNT(*) FROM {tabel}")
    print(tabel, ":", cursor.fetchone()[0])

conn.close()
