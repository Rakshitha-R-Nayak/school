from flask import Flask, render_template, request, redirect
import mysql.connector

app = Flask(__name__)

# Connect to MySQL database
def connect_to_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",  # Use your MySQL password
        database="student-management-system"
    )

@app.route("/")
def index():
    return render_template("index.html")

# Add a student
@app.route("/add", methods=["GET", "POST"])
def add_student():
    if request.method == "POST":
        name = request.form["name"]
        roll_number = request.form["roll_number"]
        student_class = request.form["class"]
        age = request.form["age"]

        db = connect_to_db()
        cursor = db.cursor()
        query = "INSERT INTO students (name, roll_number, class, age) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (name, roll_number, student_class, age))
        db.commit()
        db.close()

        return redirect("/")
    return render_template("add_student.html")

# View all students
@app.route("/view")
def view_students():
    db = connect_to_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()
    db.close()
    return render_template("view_students.html", students=students)
@app.route("/update/<int:student_id>", methods=["GET", "POST"])
def update_student(student_id):
    db = connect_to_db()
    cursor = db.cursor()

    if request.method == "POST":
        name = request.form.get("name")
        age = request.form.get("age")
        roll_no = request.form.get("roll_no")
        grade = request.form.get("class")

        # Create a list for the fields that are being updated
        fields = []
        values = []

        # Only add fields that are not empty to the update query
        if name:  # Check if 'name' field is not empty
            fields.append("name = %s")
            values.append(name)
        if roll_no:  # Check if 'roll_no' field is not empty
            fields.append("roll_no = %s")
            values.append(roll_no)
        if grade:  # Check if 'grade' field is not empty
            fields.append("class = %s")
            values.append(grade)
        if age:  # Check if 'age' field is not empty
            fields.append("age = %s")
            values.append(age)

        # If no fields are provided (all are empty), return an error message
        if not fields:
            return "Please fill in at least one field."

        # Add the student_id to the values list
        values.append(student_id)

        # Construct the dynamic SQL query
        query = f"UPDATE students SET {', '.join(fields)} WHERE id = %s"
        cursor.execute(query, tuple(values))
        db.commit()
        db.close()
        return redirect("/view")

    # Fetch the student data by ID for GET request to pre-fill the form
    query = "SELECT * FROM students WHERE id = %s"
    cursor.execute(query, (student_id,))
    student = cursor.fetchone()
    db.close()

    # Pass the student data to the template for form pre-filling
    return render_template("update_student.html", student=student)



# Delete a student
@app.route("/delete/<int:student_id>")
def delete_student(student_id):
    db = connect_to_db()
    cursor = db.cursor()
    query = "DELETE FROM students WHERE id = %s"
    cursor.execute(query, (student_id,))
    db.commit()
    db.close()
    return redirect("/view")


# Add a new course
@app.route("/add_course", methods=["GET", "POST"])
def add_course():
    if request.method == "POST":
        course_name = request.form["course_name"]
        course_code = request.form["course_code"]
        teacher_id = request.form["teacher_id"]  # Assuming you want to link a teacher to the course

        db = connect_to_db()
        cursor = db.cursor()
        query = "INSERT INTO courses (course_name, course_code, teacher_id) VALUES (%s, %s, %s)"
        cursor.execute(query, (course_name, course_code, teacher_id))
        db.commit()
        db.close()

        return redirect("/view_courses")  # Redirect to a page to view all courses
    return render_template("add_course.html")  # Template to add a course


# View all courses
@app.route("/view_courses")
def view_courses():
    db = connect_to_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM courses")
    courses = cursor.fetchall()
    db.close()
    return render_template("view_courses.html", courses=courses)  # Pass courses to a template to display


# Add a new teacher
@app.route("/add_teacher", methods=["GET", "POST"])
def add_teacher():
    if request.method == "POST":
        name = request.form["name"]
        subject = request.form["subject"]

        db = connect_to_db()
        cursor = db.cursor()
        query = "INSERT INTO teachers (name, subject) VALUES (%s, %s)"
        cursor.execute(query, (name, subject))
        db.commit()
        db.close()

        return redirect("/view_teachers")  # Redirect to a page to view all teachers
    return render_template("add_teacher.html")  # Template to add a teacher



# View all teachers
@app.route("/view_teachers")
def view_teachers():
    db = connect_to_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM teachers")
    teachers = cursor.fetchall()
    db.close()
    return render_template("view_teachers.html", teachers=teachers)  # Pass teachers to a template to display


@app.route("/add_marks", methods=["GET", "POST"])
def add_marks():
    db = connect_to_db()
    cursor = db.cursor()
    
    if request.method == "POST":
        student_id = request.form["student_id"]
        subject = request.form["subject"]
        marks = request.form["marks"]

        # Insert the marks into the marks table
        query = "INSERT INTO marks (student_id, subject, marks) VALUES (%s, %s, %s)"
        cursor.execute(query, (student_id, subject, marks))
        db.commit()
        db.close()
        return redirect("/view_marks")
    
    # Fetch all students for dropdown
    cursor.execute("SELECT id, name FROM students")
    students = cursor.fetchall()
    db.close()
    return render_template("add_marks.html", students=students)

@app.route("/view_marks")
def view_marks():
    db = connect_to_db()
    cursor = db.cursor()

    # Query to fetch marks with student names
    query = """
        SELECT marks.id, students.name, marks.subject, marks.marks 
        FROM marks
        INNER JOIN students ON marks.student_id = students.id
    """
    cursor.execute(query)
    marks = cursor.fetchall()
    db.close()
    return render_template("view_marks.html", marks=marks)

if __name__ == "__main__":
    app.run(debug=True)
