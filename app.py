from flask import Flask, render_template, request, redirect, url_for, session, flash
from datetime import datetime
import database

app = Flask(__name__)
app.secret_key = 'super_secret_hackathon_key'

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/book_appointment', methods=['GET', 'POST'])
def book_appointment_public():
    doctors = database.get_doctors()
    
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = 'patient_default' # Simple placeholder for unauthenticated
        age = request.form['age']
        gender = request.form['gender']
        phone = request.form['phone']
        address = request.form['address']
        
        doctor_id = request.form['doctor']
        appt_date = request.form['appointment_date']
        appt_time = request.form['appointment_time']
        
        try:
            patient_id = database.create_patient(name, email, password, age, gender, phone, address)
            success, msg = database.book_appointment(
                patient_id, doctor_id, None, appt_date, appt_time
            )
            
            if success:
                flash(f"Appointment booked successfully for {name}!", "success")
                return redirect(url_for('home'))
            else:
                flash(f"Booking failed: {msg}", "error")
        except Exception as e:
            flash(f"Error booking appointment: {str(e)}", "error")
            
    return render_template('book_appointment.html', doctors=doctors)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        user = database.get_user_by_email(email)
        
        if user and user['password'] == password:
            session['user_id'] = user['id']
            session['user_role'] = user['role']
            session['user_name'] = user['name']
            
            if user['role'] == 'receptionist':
                rec = database.get_receptionist_by_user_id(user['id'])
                if rec:
                    session['reception_id'] = rec['id']
                return redirect(url_for('receptionist_dashboard'))
            elif user['role'] == 'doctor':
                doc = database.get_doctor_by_user_id(user['id'])
                if doc:
                    session['doctor_id'] = doc['id']
                return redirect(url_for('doctor_dashboard'))
            else:
                flash("Role not supported yet.", "error")
        else:
            flash("Invalid email or password", "error")
            
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/receptionist', methods=['GET', 'POST'])
def receptionist_dashboard():
    if 'user_id' not in session or session['user_role'] != 'receptionist':
        return redirect(url_for('login'))
        
    doctors = database.get_doctors()
    
    if request.method == 'POST':
        # Handles submitting the admit and book form
        action = request.form.get('action')
        
        if action == 'admit_and_book':
            # Patient details
            name = request.form['name']
            email = request.form['email']
            password = 'password123' # Default for demonstration
            age = request.form['age']
            gender = request.form['gender']
            phone = request.form['phone']
            address = request.form['address']
            
            # Appointment details
            doctor_id = request.form['doctor']
            appt_date = request.form['appointment_date']
            appt_time = request.form['appointment_time']
            
            try:
                # 1. Admit patient
                patient_id = database.create_patient(name, email, password, age, gender, phone, address)
                
                # 2. Book appointment with validation
                success, msg = database.book_appointment(
                    patient_id, doctor_id, session.get('reception_id'), appt_date, appt_time
                )
                
                if success:
                    flash(f"Patient {name} admitted and appointment booked successfully!", "success")
                else:
                    flash(f"Error booking appointment for {name}: {msg}", "error")
            except Exception as e:
                flash(f"Error admitting patient: {str(e)}", "error")
                
        return redirect(url_for('receptionist_dashboard'))
        
    return render_template('receptionist.html', doctors=doctors)

@app.route('/doctor', methods=['GET'])
def doctor_dashboard():
    if 'user_id' not in session or session['user_role'] != 'doctor':
        return redirect(url_for('login'))
        
    doctor_id = session.get('doctor_id')
    today_date = datetime.now().strftime('%Y-%m-%d')
    appointments = database.get_appointments_for_doctor(doctor_id, today_date)
    
    return render_template('doctor.html', appointments=appointments, today=today_date)

@app.route('/prescription/<int:appointment_id>', methods=['GET', 'POST'])
def prescription(appointment_id):
    if 'user_id' not in session or session['user_role'] != 'doctor':
        return redirect(url_for('login'))
        
    appt = database.get_appointment_details(appointment_id)
    if not appt:
        flash("Appointment not found.", "error")
        return redirect(url_for('doctor_dashboard'))
        
    if request.method == 'POST':
        diagnosis = request.form['diagnosis']
        medicines = request.form['medicines']
        notes = request.form['notes']
        
        success = database.update_prescription(appointment_id, diagnosis, medicines, notes)
        if success:
            flash("Prescription updated successfully. Status changed to completed.", "success")
            return redirect(url_for('doctor_dashboard'))
        else:
            flash("Failed to update prescription.", "error")
            
    return render_template('prescription.html', appt=appt)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
