from flask import Flask, render_template
import csv
import json

app = Flask(__name__)

@app.route('/')
def dashboard():
    # Read CSV using csv module
    students = []
    with open('exam_results.csv', 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            row['Math'] = float(row['Math'])
            row['Science'] = float(row['Science'])
            row['English'] = float(row['English'])
            row['History'] = float(row['History'])
            students.append(row)

    # Calculate average scores per subject
    subject_averages = {}
    subjects = ['Math', 'Science', 'English', 'History']
    for subject in subjects:
        subject_averages[subject] = sum(s[subject] for s in students) / len(students)

    # Calculate overall average per student and pass/fail
    for student in students:
        student['Average'] = sum(student[sub] for sub in subjects) / len(subjects)
        student['Pass'] = student['Average'] >= 70

    pass_count = sum(1 for s in students if s['Pass'])
    pass_rate = (pass_count / len(students)) * 100
    fail_rate = 100 - pass_rate

    # Trends: average score by exam date
    date_groups = {}
    for student in students:
        date = student['Exam_Date']
        if date not in date_groups:
            date_groups[date] = []
        date_groups[date].append(student['Average'])
    trends = {date: sum(averages) / len(averages) for date, averages in date_groups.items()}

    # Subject-wise performance: count of passes per subject (score >= 70)
    subject_passes = {}
    for subject in subjects:
        subject_passes[subject] = sum(1 for s in students if s[subject] >= 70)

    return render_template('index.html',
                           subject_averages=subject_averages,
                           pass_rate=pass_rate,
                           fail_rate=fail_rate,
                           trends=trends,
                           subject_passes=subject_passes,
                           students=students)

if __name__ == '__main__':
    app.run(debug=True)
