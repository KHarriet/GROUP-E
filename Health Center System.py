import sqlite3

# Initialize the database
def initialize_database():
    conn = sqlite3.connect('health_center.db')
    cursor = conn.cursor()
    
    # Create patients table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS patients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        )
    ''')

    # Create appointments table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS appointments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id INTEGER,
            doctor_name TEXT NOT NULL,
            date_time TEXT NOT NULL,
            FOREIGN KEY (patient_id) REFERENCES patients (id)
        )
    ''')

    # Create prescriptions table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS prescriptions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id INTEGER,
            details TEXT NOT NULL,
            FOREIGN KEY (patient_id) REFERENCES patients (id)
        )
    ''')

    conn.commit()
    conn.close()

# Main function to run the system
def main():
    initialize_database()

    while True:
        user_input = get_user_input()

        if user_input == "patient":
            handle_patient_request()
        elif user_input == "doctor":
            handle_doctor_request()
        elif user_input == "receptionist":
            handle_receptionist_request()
        else:
            print("Invalid input. Please enter 'patient', 'doctor', or 'receptionist'.")

# Function to get user input
def get_user_input():
    return input("Enter your role (patient, doctor, receptionist) or 'exit' to quit: ").strip().lower()

# Functions for patient requests
def handle_patient_request():
    print("\n--- Patient Menu ---")
    action = input("Choose an action (register, book appointment, check-in): ").strip().lower()

    if action == "register":
        name = input("Enter your name: ")
        register_patient(name)
    elif action == "book appointment":
        patient_id = int(input("Enter your Patient ID: "))
        doctor_name = input("Enter Doctor's Name: ")
        date_time = input("Enter Appointment Date and Time (YYYY-MM-DD HH:MM): ")
        schedule_appointment(patient_id, doctor_name, date_time)
    elif action == "check-in":
        patient_id = int(input("Enter your Patient ID: "))
        check_in_patient(patient_id)
    else:
        print("Invalid action.")

# Functions for doctor requests
def handle_doctor_request():
    print("\n--- Doctor Menu ---")
    action = input("Choose an action (manage appointment, record prescription): ").strip().lower()

    if action == "manage appointment":
        appointment_id = int(input("Enter Appointment ID to cancel: "))
        cancel_appointment(appointment_id)
    elif action == "record prescription":
        patient_id = int(input("Enter Patient ID: "))
        prescription_details = input("Enter Prescription Details: ")
        record_prescription(patient_id, prescription_details)
    else:
        print("Invalid action.")

# Functions for receptionist requests
def handle_receptionist_request():
    print("\n--- Receptionist Menu ---")
    action = input("Choose an action (register patient, schedule appointment): ").strip().lower()

    if action == "register patient":
        name = input("Enter patient's name: ")
        register_patient(name)
    elif action == "schedule appointment":
        patient_id = int(input("Enter Patient ID: "))
        doctor_name = input("Enter Doctor's Name: ")
        date_time = input("Enter Appointment Date and Time (YYYY-MM-DD HH:MM): ")
        schedule_appointment(patient_id, doctor_name, date_time)
    else:
        print("Invalid action.")

# Database functions
def register_patient(name):
    conn = sqlite3.connect('health_center.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO patients (name) VALUES (?)', (name,))
    conn.commit()
    conn.close()
    print(f"Patient {name} registered successfully.")

def schedule_appointment(patient_id, doctor_name, date_time):
    conn = sqlite3.connect('health_center.db')
    cursor = conn.cursor()
    
    cursor.execute('INSERT INTO appointments (patient_id, doctor_name, date_time) VALUES (?, ?, ?)',
                   (patient_id, doctor_name, date_time))
    
    conn.commit()
    conn.close()
    
    print(f"Appointment scheduled for Patient ID {patient_id} with Dr. {doctor_name} on {date_time}.")

def check_in_patient(patient_id):
    conn = sqlite3.connect('health_center.db')
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM patients WHERE id = ?', (patient_id,))
    
    if cursor.fetchone():
        print(f"Patient ID {patient_id} checked in successfully.")
    else:
        print("Patient not found.")
    
    conn.close()

def cancel_appointment(appointment_id):
    conn = sqlite3.connect('health_center.db')
    cursor = conn.cursor()
    
    cursor.execute('DELETE FROM appointments WHERE id = ?', (appointment_id,))
    
    if cursor.rowcount > 0:
        print(f"Appointment ID {appointment_id} canceled successfully.")
    else:
        print("Appointment not found.")
    
    conn.commit()
    conn.close()

def record_prescription(patient_id, prescription_details):
    conn = sqlite3.connect('health_center.db')
    cursor = conn.cursor()
    
    cursor.execute('INSERT INTO prescriptions (patient_id, details) VALUES (?, ?)',
                   (patient_id, prescription_details))
    
    conn.commit()
    conn.close()
    
    print(f"Prescription recorded for Patient ID {patient_id}.")

if __name__ == "__main__":
   main()