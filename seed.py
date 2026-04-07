import sqlite3
import os

DB_PATH = 'unified_hospital.db'

def seed_database():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Clear existing data to be safe for re-seeding
    cursor.execute("DELETE FROM users")
    cursor.execute("DELETE FROM doctors")
    cursor.execute("DELETE FROM receptionists")
    cursor.execute("DELETE FROM patients")
    cursor.execute("DELETE FROM appointments")
    
    # 1. Add Receptionist User
    cursor.execute("""
        INSERT INTO users (name, email, password, role)
        VALUES ('Alice Admin', 'receptionist@hospital.com', 'password123', 'receptionist')
    """)
    receptionist_user_id = cursor.lastrowid
    
    cursor.execute("""
        INSERT INTO receptionists (user_id) VALUES (?)
    """, (receptionist_user_id,))
    
    # 2. Add Doctor User
    cursor.execute("""
        INSERT INTO users (name, email, password, role)
        VALUES ('Dr. Smith', 'doctor@hospital.com', 'password123', 'doctor')
    """)
    doctor_user_id = cursor.lastrowid
    
    cursor.execute("""
        INSERT INTO doctors (user_id, specialization, available_time, fee, mode)
        VALUES (?, 'Cardiologist', '09:00-17:00', 500.0, 'offline')
    """, (doctor_user_id,))
    
    conn.commit()
    conn.close()
    print("Database seeded successfully with dummy Receptionist and Doctor.")

if __name__ == '__main__':
    seed_database()
