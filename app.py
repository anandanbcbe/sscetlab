from flask import Flask, render_template, request, redirect, url_for, session
import csv
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'secretkey'  # Required to use sessions

# Department schedule
schedule = {1: "IT", 2: "AGRI", 3: "MECH", 4: "CS", 5: "IT", 6: "AGRI", 7: "MECH"}

# CSV base path
csv_base_path = "C:/Users/Admin/Desktop/"  # Update this path to the location of your CSV files

# Get current day of the week (1 for Monday, 7 for Sunday)
def get_current_day():
    return datetime.now().isoweekday()

# Read student data from the department's CSV file
def read_csv(department):
    filename = f"{csv_base_path}{department.lower()}.csv"
    try:
        with open(filename, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            return [row for row in reader], filename
    except FileNotFoundError:
        return [], None

# Write updated student data back to the CSV file
def write_csv(student_data, filename):
    keys = student_data[0].keys()
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=keys)
        writer.writeheader()
        writer.writerows(student_data)

@app.route("/", methods=['GET', 'POST'])
def index():
    current_day = get_current_day()
    department_today = schedule.get(current_day)

    if request.method == 'POST':
        reg_num = request.form['reg_num']
        student_data, filename = read_csv(department_today)

        if student_data:
            student = next((s for s in student_data if s["RegNum"] == reg_num), None)
            if student:
                student["Department"] = department_today  # Ensure department is added
                session['student'] = student  # Save student info in the session
                session['filename'] = filename
                return redirect(url_for('lab_exercise'))
            else:
                return render_template('index.html', error="Student not found.", department=department_today)

    return render_template('index.html', department=department_today)

@app.route("/lab_exercise", methods=['GET', 'POST'])
def lab_exercise():
    if 'student' not in session:
        return redirect(url_for('index'))

    student = session['student']

    if request.method == 'POST':
        output = request.form['output']
        filename = session['filename']
        student_data, _ = read_csv(student['Department'])  # Fetch data based on Department
        stored_student = next((s for s in student_data if s["RegNum"] == student['RegNum']), None)

        if stored_student and output == stored_student['LabOutput']:
            stored_student["Marks"] = "5"  # Add 5 marks if output matches
            stored_student["SubmittedTime"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Add system time
            write_csv(student_data, filename)
            return render_template('success.html', message="Correct! You get 5 marks.")
        else:
            return render_template('error.html', message="Incorrect output.")

    return render_template('lab_exercise.html', student=student)

@app.route("/success")
def success():
    return render_template('success.html')

@app.route("/error")
def error():
    return render_template('error.html')

if __name__ == "__main__":
    app.run(debug=True)

