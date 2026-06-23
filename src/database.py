import sqlite3
from datetime import datetime
from pathlib import Path

from src.config import DATABASE_FILE


def get_connection():
    DATABASE_FILE.parent.mkdir(parents=True, exist_ok=True)
    return sqlite3.connect(DATABASE_FILE)


def init_database():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS appointments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_name TEXT NOT NULL,
            patient_phone TEXT NOT NULL,
            city TEXT NOT NULL,
            specialty TEXT NOT NULL,
            clinic_name TEXT NOT NULL,
            doctor_name TEXT NOT NULL,
            appointment_slot TEXT NOT NULL,
            booking_code TEXT NOT NULL UNIQUE,
            status TEXT NOT NULL DEFAULT 'confirmed',
            created_at TEXT NOT NULL
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS emergency_alerts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_name TEXT NOT NULL,
            patient_phone TEXT NOT NULL,
            city TEXT NOT NULL,
            clinic_name TEXT NOT NULL,
            symptoms TEXT NOT NULL,
            urgency_level TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'sent',
            created_at TEXT NOT NULL
        )
        """
    )

    conn.commit()
    conn.close()


def save_appointment(
    patient_name,
    patient_phone,
    city,
    specialty,
    clinic_name,
    doctor_name,
    appointment_slot,
    booking_code,
):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO appointments (
            patient_name,
            patient_phone,
            city,
            specialty,
            clinic_name,
            doctor_name,
            appointment_slot,
            booking_code,
            status,
            created_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            patient_name,
            patient_phone,
            city,
            specialty,
            clinic_name,
            doctor_name,
            appointment_slot,
            booking_code,
            "confirmed",
            datetime.now().isoformat(timespec="seconds"),
        ),
    )

    conn.commit()
    appointment_id = cursor.lastrowid
    conn.close()

    return appointment_id


def save_emergency_alert(
    patient_name,
    patient_phone,
    city,
    clinic_name,
    symptoms,
    urgency_level,
):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO emergency_alerts (
            patient_name,
            patient_phone,
            city,
            clinic_name,
            symptoms,
            urgency_level,
            status,
            created_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            patient_name,
            patient_phone,
            city,
            clinic_name,
            symptoms,
            urgency_level,
            "sent",
            datetime.now().isoformat(timespec="seconds"),
        ),
    )

    conn.commit()
    alert_id = cursor.lastrowid
    conn.close()

    return alert_id


def get_all_appointments():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            id,
            patient_name,
            patient_phone,
            city,
            specialty,
            clinic_name,
            doctor_name,
            appointment_slot,
            booking_code,
            status,
            created_at
        FROM appointments
        ORDER BY id DESC
        """
    )

    rows = cursor.fetchall()
    conn.close()

    return rows


def get_all_emergency_alerts():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            id,
            patient_name,
            patient_phone,
            city,
            clinic_name,
            symptoms,
            urgency_level,
            status,
            created_at
        FROM emergency_alerts
        ORDER BY id DESC
        """
    )

    rows = cursor.fetchall()
    conn.close()

    return rows


if __name__ == "__main__":
    init_database()
    print("DATABASE_READY")