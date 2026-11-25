
import sqlite3

DATABASE = "database.db"

def buat_database():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    # 1. Tabel aktivitas login dan logout
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS logon_events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            event_date DATETIME NOT NULL,
            user_id TEXT NOT NULL,
            pc TEXT,
            activity TEXT NOT NULL
        )
    """)

    # 2. Tabel aktivitas perangkat
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS device_events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            event_date DATETIME NOT NULL,
            user_id TEXT NOT NULL,
            pc TEXT,
            activity TEXT NOT NULL
        )
    """)

    # 3. Tabel fitur aktivitas pengguna
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS activity_features (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT NOT NULL,
            activity_date DATE NOT NULL,
            login_count INTEGER DEFAULT 0,
            logoff_count INTEGER DEFAULT 0,
            after_hours_login INTEGER DEFAULT 0,
            unique_pc INTEGER DEFAULT 0,
            device_connect INTEGER DEFAULT 0,
            device_disconnect INTEGER DEFAULT 0,
            UNIQUE(user_id, activity_date)
        )
    """)

    # 4. Tabel riwayat pelatihan model
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS model_runs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            model_name TEXT NOT NULL,
            algorithm TEXT NOT NULL,
            trained_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            status TEXT
        )
    """)

    # 5. Tabel hasil deteksi
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS detection_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            feature_id INTEGER NOT NULL,
            model_run_id INTEGER NOT NULL,
            prediction TEXT NOT NULL,
            anomaly_score REAL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY (feature_id)
                REFERENCES activity_features(id),

            FOREIGN KEY (model_run_id)
                REFERENCES model_runs(id)
        )
    """)

    # Index untuk mempercepat pencarian
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_logon_user
        ON logon_events(user_id)
    """)

    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_device_user
        ON device_events(user_id)
    """)

    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_features_user_date
        ON activity_features(user_id, activity_date)
    """)

    conn.commit()
    conn.close()

    print("Database berhasil disiapkan!")
    print("5 tabel utama berhasil dibuat.")
    print("Tabel lama tetap dipertahankan.")

if __name__ == "__main__":
    buat_database()
