
import sqlite3
import shutil
import os

DATABASE = "database.db"
BACKUP = "database_sebelum_migrasi.db"


def rapikan_database():
    # Pastikan database tersedia
    if not os.path.exists(DATABASE):
        print("Database tidak ditemukan!")
        return

    # Buat backup sebelum migrasi
    if not os.path.exists(BACKUP):
        shutil.copy2(DATABASE, BACKUP)
        print("Backup berhasil dibuat:", BACKUP)
    else:
        print("Backup sudah tersedia:", BACKUP)

    conn = sqlite3.connect(DATABASE)
    conn.execute("PRAGMA foreign_keys = ON")
    cursor = conn.cursor()

    try:
        # Pastikan struktur lama sesuai hasil pemeriksaan
        cursor.execute("PRAGMA table_info(labeled_features)")
        kolom = [row[1] for row in cursor.fetchall()]

        if "feature_id" in kolom:
            print("Tabel labeled_features sudah menggunakan feature_id.")
            return

        if not kolom:
            raise Exception("Tabel labeled_features tidak ditemukan.")

        # Hitung jumlah data label lama
        cursor.execute("SELECT COUNT(*) FROM labeled_features")
        jumlah_lama = cursor.fetchone()[0]

        # Pastikan semua label memiliki pasangan fitur
        cursor.execute("""
            SELECT COUNT(*)
            FROM labeled_features l
            LEFT JOIN activity_features f
                ON l.user_id = f.user_id
                AND l.activity_date = f.activity_date
            WHERE f.id IS NULL
        """)
        tidak_cocok = cursor.fetchone()[0]

        if tidak_cocok > 0:
            raise Exception(
                f"Ada {tidak_cocok} data label yang tidak memiliki pasangan fitur."
            )

        # Buat tabel baru dengan relasi
        cursor.execute("""
            CREATE TABLE labeled_features_new (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                feature_id INTEGER NOT NULL UNIQUE,
                label INTEGER NOT NULL CHECK(label IN (0, 1)),
                FOREIGN KEY (feature_id)
                    REFERENCES activity_features(id)
            )
        """)

        # Hubungkan label dengan fitur berdasarkan user dan tanggal
        cursor.execute("""
            INSERT INTO labeled_features_new (feature_id, label)
            SELECT f.id, l.label
            FROM labeled_features l
            JOIN activity_features f
                ON l.user_id = f.user_id
                AND l.activity_date = f.activity_date
        """)

        jumlah_baru = cursor.rowcount

        if jumlah_baru != jumlah_lama:
            raise Exception(
                f"Jumlah data berubah: lama {jumlah_lama}, baru {jumlah_baru}"
            )

        # Ganti tabel lama setelah data berhasil dicocokkan
        cursor.execute("DROP TABLE labeled_features")
        cursor.execute("""
            ALTER TABLE labeled_features_new
            RENAME TO labeled_features
        """)

        cursor.execute("""
            CREATE INDEX idx_labeled_feature
            ON labeled_features(feature_id)
        """)

        conn.commit()

        print("\nMIGRASI BERHASIL!")
        print("Jumlah label lama:", jumlah_lama)
        print("Jumlah label baru:", jumlah_baru)
        print("Relasi feature_id berhasil dibuat.")

    except Exception as error:
        conn.rollback()
        print("\nMIGRASI DIBATALKAN!")
        print("Alasan:", error)

    finally:
        conn.close()


if __name__ == "__main__":
    rapikan_database()
