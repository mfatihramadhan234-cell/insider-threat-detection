
import sqlite3
import pandas as pd

conn = sqlite3.connect("database.db")

df = pd.read_sql_query("""
    SELECT user_id, COUNT(*) AS jumlah
    FROM labeled_features
    WHERE label = 1
    GROUP BY user_id
    ORDER BY jumlah DESC
""", conn)

print("Jumlah pengguna dengan label 1:", len(df))
print("\n10 pengguna dengan data insiden terbanyak:")
print(df.head(10).to_string(index=False))

print("\nStatistik distribusi:")
print(df["jumlah"].describe())

conn.close()
