import sqlite3

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

try:
    cursor.execute("DROP INDEX IF EXISTS idx_logon_source")
    cursor.execute("DROP INDEX IF EXISTS idx_device_source")

    conn.commit()

    print("Index duplikat berhasil dihapus.")
    print("Index UNIQUE utama tetap dipertahankan.")

except sqlite3.Error as error:
    conn.rollback()
    print("Terjadi kesalahan:", error)

finally:
    conn.close()