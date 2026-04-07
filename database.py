import sqlite3

DB_PATH = 'hospital.db'

def get_db_connection():
    conn = sqlite3.connect(DB_PATH, timeout=15.0, check_same_thread=False)
    conn.execute('PRAGMA journal_mode=WAL;')
    conn.row_factory = sqlite3.Row
    return conn

def get_user_by_email(email):
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()
    conn.close()
    return user

def create_patient(name, email, password, age, gender, phone, address):
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        
        # Check if email is somewhat unique, or we just rely on users table unique constraint if there is one
        cursor.execute("INSERT INTO users (name, email, password, role) VALUES (?, ?, ?, 'patient')", 
                       (name, email, password))
        user_id = cursor.lastrowid
        
        cursor.execute("INSERT INTO patients (user_id, name, age, gender, phone, address) VALUES (?, ?, ?, ?, ?, ?)",
                       (user_id, name, age, gender, phone, address))
        patient_id = cursor.lastrowid
        
        conn.commit()
        return patient_id
    except sqlite3.Error as e:
        conn.rollback()
        raise e
    finally:
        conn.close()

def book_appointment(patient_id, doctor_id, reception_id, date, time):
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        
        # Check for double booking
        cursor.execute('''
            SELECT id FROM appointments 
            WHERE doctor_id = ? AND appointment_date = ? AND appointment_time = ? AND status != 'cancelled'
        ''', (doctor_id, date, time))
        existing_appt = cursor.fetchone()
        
        if existing_appt:
            return False, "This doctor is already booked at this date and time."
        
        cursor.execute('''
            INSERT INTO appointments (patient_id, doctor_id, reception_id, appointment_date, appointment_time, status)
            VALUES (?, ?, ?, ?, ?, 'booked')
        ''', (patient_id, doctor_id, reception_id, date, time))
        
        conn.commit()
        return True, "Appointment booked successfully."
    except sqlite3.Error as e:
        conn.rollback()
        return False, str(e)
    finally:
        conn.close()

def get_doctors():
    conn = get_db_connection()
    docs = conn.execute('''
        SELECT d.id as id, u.name as name, d.specialization as specialization, d.fee as fee
        FROM doctors d
        JOIN users u ON d.user_id = u.id
    ''').fetchall()
    conn.close()
    return docs

def get_doctor_by_user_id(user_id):
    conn = get_db_connection()
    doc = conn.execute('SELECT id FROM doctors WHERE user_id = ?', (user_id,)).fetchone()
    conn.close()
    return doc

def get_receptionist_by_user_id(user_id):
    conn = get_db_connection()
    rec = conn.execute('SELECT id FROM receptionists WHERE user_id = ?', (user_id,)).fetchone()
    conn.close()
    return rec

def get_appointments_for_doctor(doctor_id, date_limit=None):
    conn = get_db_connection()
    query = '''
        SELECT a.id, a.appointment_time, a.status, p.name as patient_name, p.age, p.gender
        FROM appointments a
        JOIN patients p ON a.patient_id = p.id
        WHERE a.doctor_id = ?
    '''
    params = [doctor_id]
    if date_limit:
        query += ' AND a.appointment_date = ?'
        params.append(date_limit)
    
    query += ' ORDER BY a.appointment_time ASC'
    
    appts = conn.execute(query, tuple(params)).fetchall()
    conn.close()
    return appts

def get_appointment_details(appointment_id):
    conn = get_db_connection()
    appt = conn.execute('''
        SELECT a.*, p.name as patient_name, p.age, p.gender, u.name as doctor_name
        FROM appointments a
        JOIN patients p ON a.patient_id = p.id
        JOIN doctors d ON a.doctor_id = d.id
        JOIN users u ON d.user_id = u.id
        WHERE a.id = ?
    ''', (appointment_id,)).fetchone()
    conn.close()
    return appt

def update_prescription(appointment_id, diagnosis, medicines, notes):
    conn = get_db_connection()
    try:
        conn.execute('''
            UPDATE appointments
            SET diagnosis = ?, medicines = ?, notes = ?, status = 'completed'
            WHERE id = ?
        ''', (diagnosis, medicines, notes, appointment_id))
        conn.commit()
        return True
    except sqlite3.Error:
        conn.rollback()
        return False
    finally:
        conn.close()
