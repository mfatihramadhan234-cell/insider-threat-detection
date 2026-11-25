
import os
import sqlite3
from flask import Flask, render_template, jsonify

app = Flask(__name__)
app.secret_key = "insider_threat_secret"

# =====================================
# KONFIGURASI DATABASE
# =====================================

DATABASE = os.path.join(app.root_path, "database.db")


# =====================================
# KONEKSI DATABASE
# =====================================

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row

    # Mengaktifkan foreign key
    conn.execute("PRAGMA foreign_keys = ON")

    return conn


# =====================================
# DASHBOARD
# =====================================

@app.route("/")
def index():
    conn = get_db_connection()

    try:
        total_logon = conn.execute("""
            SELECT COUNT(*) FROM logon_events
        """).fetchone()[0]

        total_device = conn.execute("""
            SELECT COUNT(*) FROM device_events
        """).fetchone()[0]

        total_users = conn.execute("""
            SELECT COUNT(DISTINCT user_id)
            FROM logon_events
        """).fetchone()[0]

        recent_logon = conn.execute("""
            SELECT event_date, user_id, pc, activity
            FROM logon_events
            ORDER BY event_date DESC
            LIMIT 10
        """).fetchall()

        statistik = {
            "total_logon": total_logon,
            "total_device": total_device,
            "total_users": total_users
        }

        return render_template(
            "index.html",
            statistik=statistik,
            recent_logon=recent_logon
        )

    finally:
        conn.close()


# =====================================
# MENU DATA AKTIVITAS
# =====================================

@app.route("/aktivitas")
def aktivitas():
    conn = get_db_connection()

    try:
        logon = conn.execute("""
            SELECT event_date, user_id, pc, activity
            FROM logon_events
            ORDER BY event_date DESC
            LIMIT 100
        """).fetchall()

        device = conn.execute("""
            SELECT event_date, user_id, pc, activity
            FROM device_events
            ORDER BY event_date DESC
            LIMIT 100
        """).fetchall()

        return render_template(
            "aktivitas.html",
            logon=logon,
            device=device
        )

    finally:
        conn.close()


# =====================================
# MENU DETEKSI ANOMALI
# =====================================

@app.route("/deteksi")
def deteksi():
    conn = get_db_connection()

    try:
        total_fitur = conn.execute("""
            SELECT COUNT(*) FROM activity_features
        """).fetchone()[0]

        return render_template(
            "deteksi.html",
            total_fitur=total_fitur
        )

    finally:
        conn.close()


# =====================================
# MENU HASIL DETEKSI
# =====================================

@app.route("/hasil")
def hasil():
    conn = get_db_connection()

    try:
        hasil_deteksi = conn.execute("""
            SELECT
                d.id,
                f.user_id,
                f.activity_date,
                d.prediction,
                d.anomaly_score,
                d.created_at
            FROM detection_results d
            JOIN activity_features f
                ON d.feature_id = f.id
            ORDER BY d.created_at DESC
            LIMIT 100
        """).fetchall()

        return render_template(
            "hasil.html",
            hasil_deteksi=hasil_deteksi
        )

    finally:
        conn.close()


# =====================================
# API STATISTIK
# =====================================

@app.route("/api/statistik")
def api_statistik():
    conn = get_db_connection()

    try:
        data = {
            "logon": conn.execute("""
                SELECT COUNT(*) FROM logon_events
            """).fetchone()[0],

            "device": conn.execute("""
                SELECT COUNT(*) FROM device_events
            """).fetchone()[0],

            "users": conn.execute("""
                SELECT COUNT(DISTINCT user_id)
                FROM logon_events
            """).fetchone()[0],

            "fitur": conn.execute("""
                SELECT COUNT(*) FROM activity_features
            """).fetchone()[0],

            "label": conn.execute("""
                SELECT COUNT(*) FROM labeled_features
            """).fetchone()[0],

            "hasil_deteksi": conn.execute("""
                SELECT COUNT(*) FROM detection_results
            """).fetchone()[0]
        }

        return jsonify(data)

    finally:
        conn.close()


# =====================================
# MENJALANKAN APLIKASI
# =====================================

if __name__ == "__main__":
    app.run(
        debug=True,
        host="0.0.0.0",
        port=5000
    )
