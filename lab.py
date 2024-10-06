import csv
import time
import pyttsx3
from datetime import datetime

# Departments schedule
schedule = {1: "IT", 2: "AGRI", 3: "MECH", 4: "CS", 5: "IT", 6: "AGRI", 7: "MECH"}

# CSV base path
csv_base_path = "C:/Users/Admin/Desktop/"

# Initialize pyttsx3 for text-to-speech
engine = pyttsx3.init()

# Function to speak text
def speak_text(text):
    print(text)
    engine.say(text)
    engine.runAndWait()

# Get the current day of the week (1=Monday, 7=Sunday)
def get_current_day():
    return datetime.now().isoweekday()

# Read department CSV file
def read_csv(department):
    filename = f"{csv_base_path}{department.lower()}.csv"
    try:
        with open(filename, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            return [row for row in reader], filename
    except FileNotFoundError:
        speak_text(f"Error: {filename} not found.")
        return [], None

# Update the CSV file with marks
def write_csv(student_data, filename):
    keys = student_data[0].keys()
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=keys)
        writer.writeheader()
        writer.writerows(student_data)

# Main function to run the lab schedule
def run_lab():
    current_day = get_current_day()
    department_today = schedule.get(current_day)

    speak_text(f"Today's department: {department_today}")
    student_data, filename = read_csv(department_today)

    if student_data:
        reg_num = input("Enter your registration number: ")
        student = next((s for s in student_data if s["RegNum"] == reg_num), None)

        if student:
            speak_text(f"Your lab exercise: {student['LabExercise']}")
            speak_text("Starting lab... Time allotted: 2 minutes.")
            time.sleep(2 * 60)  # 2 minutes timer (simplified)

            output = input("Enter the lab output: ")
            if output == student["LabOutput"]:
                speak_text("Correct! You get 5 marks.")
                student["Marks"] = "5"
                write_csv(student_data, filename)
            else:
                speak_text("Incorrect output. No marks awarded.")
        else:
            speak_text("Student not found.")

run_lab()
