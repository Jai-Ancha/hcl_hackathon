# Unified Hospital Management System (UnifiedHMS)

UnifiedHMS is a web-based Hospital Management System developed using Flask and SQLite. It provides a secure, reliable, and user-friendly portal for patients, doctors, and receptionists.

## Features

- **Public Appointment Booking**: Patients can easily book an appointment with their required doctor and receive availability status.
- **Role-based Authentication**: Secure portals tailored for Receptionists and Doctors.
- **Receptionist Dashboard**: Receptionists can manage and admit new patients, and handle their appointment bookings seamlessly.
- **Doctor's Portal**: Doctors have dedicated access to their schedules, patient lists for the day, and tools to write prescriptions (diagnoses, medicines, notes).
- **Concurrency Support**: Database fully configured with Write-Ahead Logging (WAL) to completely prevent locking issues during heavy simultaneous use.

## Technology Stack

- **Backend**: Python, Flask
- **Database**: SQLite3 (WAL mode)
- **Frontend**: HTML5, Vanilla CSS

## Setup and Installation

1. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. The SQLite database `hospital.db` is already loaded with initial seed details.
3. Run the Flask development server:
   ```bash
   python app.py
   ```
4. Navigate to `http://127.0.0.1:5000/` in your browser.

## Recent Updates
- Resolved the `database is locked` error by enabling WAL mode directly in the SQLite connection.
- Migrated data safely to a fresh `hospital.db` to resolve prior active lock corruption.
- Cleaned up the `/login` user interface by removing hard-coded placeholder credentials and hints for better professional aesthetics.

