from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = "secret123"

# ---------------- DB ----------------
def get_db():
    conn = sqlite3.connect("hospital.db")
    conn.row_factory = sqlite3.Row
    return conn

# ---------------- CREATE TABLES ----------------
def create_tables():
    conn = get_db()

    conn.execute('''
    CREATE TABLE IF NOT EXISTS doctors (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        specialization TEXT,
        username TEXT,
        password TEXT
    )
    ''')

    conn.execute('''
    CREATE TABLE IF NOT EXISTS patients (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        age INTEGER,
        problem TEXT
    )
    ''')

    conn.execute('''
    CREATE TABLE IF NOT EXISTS appointments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_id INTEGER,
        doctor_id INTEGER,
        time TEXT,
        status TEXT DEFAULT 'pending',
        prescription TEXT
    )
    ''')

    conn.commit()
    conn.close()

create_tables()

# ---------------- INSERT DOCTORS (RUN ONCE) ----------------
def insert_doctors():
    conn = get_db()

    existing = conn.execute("SELECT COUNT(*) as count FROM doctors").fetchone()

    if existing["count"] == 0:

        # ---------------- CARDIOLOGY ----------------
        cardiology = [
            ("Dr. Raj", "Cardiology", "raj", "123"),
            ("Dr. Meena", "Cardiology", "meena", "123"),
            ("Dr. Arjun", "Cardiology", "arjun", "123"),
            ("Dr. Kavya", "Cardiology", "kavya", "123"),
            ("Dr. Ramesh", "Cardiology", "ramesh", "123"),
            ("Dr. Sneha", "Cardiology", "sneha", "123"),
            ("Dr. Vikram", "Cardiology", "vikram", "123")
        ]

        # ---------------- DERMATOLOGY ----------------
        dermatology = [
            ("Dr. Priya", "Dermatology", "priya", "123"),
            ("Dr. Rahul", "Dermatology", "rahul", "123"),
            ("Dr. Neha", "Dermatology", "neha", "123"),
            ("Dr. Kiran", "Dermatology", "kiran", "123"),
            ("Dr. Anjali", "Dermatology", "anjali", "123"),
            ("Dr. Mohan", "Dermatology", "mohan", "123"),
            ("Dr. Divya", "Dermatology", "divya", "123")
        ]

        # ---------------- NEUROLOGY ----------------
        neurology = [
            ("Dr. Suresh", "Neurology", "suresh", "123"),
            ("Dr. Anil", "Neurology", "anil", "123"),
            ("Dr. Pooja", "Neurology", "pooja", "123"),
            ("Dr. Deepak", "Neurology", "deepak", "123"),
            ("Dr. Swathi", "Neurology", "swathi", "123"),
            ("Dr. Naveen", "Neurology", "naveen", "123"),
            ("Dr. Lakshmi", "Neurology", "lakshmi", "123")
        ]

        # ---------------- ORTHOPEDICS ----------------
        orthopedics = [
            ("Dr. Reddy", "Orthopedics", "reddy", "123"),
            ("Dr. Mahesh", "Orthopedics", "mahesh", "123"),
            ("Dr. Teja", "Orthopedics", "teja", "123"),
            ("Dr. Harish", "Orthopedics", "harish", "123"),
            ("Dr. Keerthi", "Orthopedics", "keerthi", "123"),
            ("Dr. Vinay", "Orthopedics", "vinay", "123"),
            ("Dr. Srikanth", "Orthopedics", "srikanth", "123")
        ]

        # Insert all doctors
        for d in cardiology + dermatology + neurology + orthopedics:
            conn.execute(
                "INSERT INTO doctors (name, specialization, username, password) VALUES (?, ?, ?, ?)", d
            )

        conn.commit()

    conn.close()

insert_doctors()

# ---------------- HOME ----------------
@app.route("/")
def index():
    return render_template("index.html")

# ---------------- ADD PATIENT ----------------
@app.route("/add_patient", methods=["GET", "POST"])
def add_patient():
    conn = get_db()

    specialization = request.args.get("specialization")

    if specialization:
        doctors = conn.execute(
            "SELECT * FROM doctors WHERE specialization=?",
            (specialization,)
        ).fetchall()
    else:
        doctors = []

    if request.method == "POST":
        name = request.form["name"]
        age = request.form["age"]
        problem = request.form["problem"]
        doctor_id = request.form["doctor"]
        time = request.form["time"]

        cur = conn.cursor()

        # Insert patient
        cur.execute(
            "INSERT INTO patients (name, age, problem) VALUES (?, ?, ?)",
            (name, age, problem)
        )
        patient_id = cur.lastrowid

        # Check slot conflict
        existing = conn.execute(
            "SELECT * FROM appointments WHERE doctor_id=? AND time=?",
            (doctor_id, time)
        ).fetchone()

        if existing:
            return "❌ Slot already booked!"

        # Insert appointment
        conn.execute(
            "INSERT INTO appointments (patient_id, doctor_id, time) VALUES (?, ?, ?)",
            (patient_id, doctor_id, time)
        )

        conn.commit()
        conn.close()
        return redirect("/")

    conn.close()
    return render_template("add_patient.html", doctors=doctors)

# ---------------- DOCTOR LOGIN ----------------
@app.route("/doctor_login", methods=["GET", "POST"])
def doctor_login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = get_db()
        doctor = conn.execute(
            "SELECT * FROM doctors WHERE username=? AND password=?",
            (username, password)
        ).fetchone()

        if doctor:
            session["doctor_id"] = doctor["id"]
            return redirect("/doctor_dashboard")
        else:
            return "❌ Invalid credentials"

    return render_template("doctor_login.html")

# ---------------- DOCTOR DASHBOARD ----------------
@app.route("/doctor_dashboard")
def doctor_dashboard():
    if "doctor_id" not in session:
        return redirect("/doctor_login")

    doctor_id = session["doctor_id"]
    conn = get_db()

    data = conn.execute('''
        SELECT a.id, p.name, p.problem, a.time, a.status, a.prescription
        FROM appointments a
        JOIN patients p ON a.patient_id = p.id
        WHERE a.doctor_id = ?
    ''', (doctor_id,)).fetchall()

    conn.close()
    return render_template("doctor_dashboard.html", data=data)

# ---------------- APPROVE ----------------
@app.route("/approve/<int:id>")
def approve(id):
    conn = get_db()
    conn.execute("UPDATE appointments SET status='approved' WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect("/doctor_dashboard")

# ---------------- PRESCRIPTION ----------------
@app.route("/prescription/<int:id>", methods=["POST"])
def prescription(id):
    text = request.form["prescription"]

    conn = get_db()
    conn.execute(
        "UPDATE appointments SET prescription=? WHERE id=?",
        (text, id)
    )
    conn.commit()
    conn.close()

    return redirect("/doctor_dashboard")

# ---------------- LOGOUT ----------------
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

# ---------------- RUN ----------------
if __name__ == "__main__":
    app.run(debug=True)