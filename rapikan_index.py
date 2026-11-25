
import sqlite3

DATABASE = "database.db"

def rapikan_index():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    try:
        cursor.execute("""
            CREATE UNIQUE INDEX IF NOT EXISTS
            idx_logon_source_id
            ON logon_events(source_id)
        """)

        cursor.execute("""
            CREATE UNIQUE INDEX IF NOT EXISTS
            idx_device_source_id
            ON device_events(source_id)
        """)

        cursor.execute("""
            CREATE INDEX IF NOT EXISTS
            idx_logon_date
            ON logon_events(event_date)
        """)

        cursor.execute("""
            CREATE INDEX IF NOT EXISTS
            idx_device_date
            ON device_events(event_date)
        """)

        conn.commit()
        print("Index berhasil dibuat!")

    except sqlite3.Error as error:
        conn.rollback()
        print("Terjadi kesalahan:", error)

    finally:
        conn.close()


if __name__ == "__main__":
    rapikan_index()
