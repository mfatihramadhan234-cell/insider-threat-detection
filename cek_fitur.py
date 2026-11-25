
import sqlite3

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

cursor.execute("""
    SELECT COUNT(*) FROM activity_features
""")
print("Total fitur:", cursor.fetchone()[0])

cursor.execute("""
    SELECT COUNT(DISTINCT user_id)
    FROM activity_features
""")
print("Jumlah pengguna:", cursor.fetchone()[0])

cursor.execute("""
    SELECT MIN(activity_date), MAX(activity_date)
    FROM activity_features
""")
print("Rentang tanggal:", cursor.fetchone())

cursor.execute("""
    SELECT *
    FROM activity_features
    LIMIT 5
""")

print("\nContoh data:")
for row in cursor.fetchall():
    print(row)

conn.close()
