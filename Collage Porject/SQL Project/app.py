from flask import Flask, request, render_template, redirect, url_for
import pyodbc

app = Flask(__name__)

# Establish a connection to the SQL Server
DRIVER_NAME = 'SQL Server'
SERVER_NAME = 'DESKTOP-TV7836E\\SQLEXPRESS'
conn = pyodbc.connect('Driver={SQL Server};'
                    'Server=DESKTOP-TV7836E\\SQLEXPRESS;'
                    'Database=university12;'
                    'Trusted_Connection=yes;')

# Create a cursor object to execute SQL queries
cursor = conn.cursor()

def get_students():
    query =\
        f'''SELECT student.NID, student.student_name, semster.semester_name, (SELECT COUNT(*) FROM courses WHERE courses.semster = student.semster)
            FROM student
            LEFT JOIN semster ON student.semster = semster.ID
            '''
    cursor.execute(query)
    results = cursor.fetchall()
    return results

def get_all_semster():
    query =\
        f'''SELECT * FROM semster
            '''
    cursor.execute(query)
    results = cursor.fetchall()
    return results

def remove_student_func(NID):
    query =\
        f'''DELETE FROM student WHERE NID = '{NID}'
            '''
    cursor.execute(query)
    conn.commit()

def save_student(NID, std_name, semster):
    query =\
        f'''UPDATE student SET student_name='{std_name}', semster='{semster}' WHERE NID = '{NID}'
            '''
    cursor.execute(query)
    conn.commit()

    return True

def add_student(NID, std_name, semster):
    query =\
        f'''INSERT INTO student VALUES ('{NID}', '{std_name}', {semster}) 
            '''
    cursor.execute(query)
    conn.commit()

def get_student(NID):
    query =\
        f'''SELECT * FROM student WHERE NID = '{NID}'
            '''
    cursor.execute(query)
    results = cursor.fetchone()
    return results

@app.route('/')
def index():
    students = get_students()
    semsters = get_all_semster()
    return render_template('students.html', students = students, semsters= semsters)

@app.route('/add_student', methods=['POST'])
def add_student_req():
    if request.method == 'POST':
        NID = request.form['nid']
        std_name = request.form['std_name']
        semster = request.form['semster']

        add_student(NID, std_name, semster)
        return redirect('/')
    
@app.route('/remove_student', methods=['GET'])
def remove_student_req():
    if request.method == 'GET':
        NID = request.args.get('NID')
        remove_student_func(NID)
        return redirect('/')

@app.route('/edit_student_page', methods=['GET'])
def edit_student_req():
    if request.method == 'GET':
        NID = request.args.get('NID')
        student = get_student(NID)
        semsters = get_all_semster()
        ret = request.args.get('ret')
        return render_template('edit-student.html', student = student, semsters= semsters, ret= ret)

@app.route('/edit_student', methods=['POST'])
def edit_student():
    if request.method == 'POST':
        NID = request.form['nid']
        std_name = request.form['std_name']
        semster = request.form['semster']

        save = save_student(NID, std_name, semster)
        return redirect(f'''/edit_student_page?NID={NID}&ret={save}''')


# Doctors

def get_all_courses():
    query =\
        f'''SELECT * FROM courses
            '''
    cursor.execute(query)
    results = cursor.fetchall()
    return results

def get_doctors():
    query =\
        f'''SELECT doctors.NID, doctors.doctor_name, doctors.salary, (SELECT COUNT(*) FROM courses WHERE courses.doctor = doctors.NID)
            FROM doctors
            LEFT JOIN courses ON doctors.NID = courses.doctor
            '''
    cursor.execute(query)
    results = cursor.fetchall()
    return results

def remove_doctor_func(NID):
    query =\
        f'''DELETE FROM doctors WHERE NID = {NID}
            '''
    cursor.execute(query)
    conn.commit()

def add_doctor(NID, name, salary):
    query =\
        f'''INSERT INTO doctors VALUES ('{NID}', '{name}', {salary})'''
    cursor.execute(query)
    conn.commit()

def get_doctor(NID):
    query =\
        f'''SELECT * FROM doctors WHERE NID = '{NID}'
            '''
    cursor.execute(query)
    results = cursor.fetchone()
    return results

def save_doctor(NID, name, salary):
    query =\
        f'''UPDATE doctors SET doctor_name='{name}', salary={salary} WHERE NID = '{NID}'
            '''
    cursor.execute(query)
    conn.commit()

    return True

@app.route('/doctors')
def doctors_page():
    doctors = get_doctors()
    courses = get_all_courses()
    return render_template('doctors.html', doctors = doctors, courses= courses)

@app.route('/remove_doctor', methods=['GET'])
def remove_doctor_req():
    if request.method == 'GET':
        NID = request.args.get('NID')
        remove_doctor_func(NID)
        return redirect('/doctors')

@app.route('/add_doctor', methods=['POST'])
def add_doctor_req():
    if request.method == 'POST':
        NID = request.form['nid']
        doctor_name = request.form['doctor_name']
        doctor_salary = request.form['doctor_salary']

        save = add_doctor(NID, doctor_name, doctor_salary)
        return redirect('/doctors')

@app.route('/edit_doctor_page', methods=['GET'])
def edit_doctor_req():
    if request.method == 'GET':
        NID = request.args.get('NID')
        doctor = get_doctor(NID)
        ret = request.args.get('ret')
        return render_template('edit-doctor.html', doctor = doctor, ret= ret)

@app.route('/edit_doctor', methods=['POST'])
def edit_doctor():
    if request.method == 'POST':
        NID = request.form['nid']
        name = request.form['doctor_name']
        salary = request.form['doctor_salary']

        save = save_doctor(NID, name, salary)
        return redirect(f'''/edit_doctor_page?NID={NID}&ret={save}''')

# SEMESTERS
def get_semsters():
    query =\
        f'''SELECT semster.ID, semster.semester_name, (SELECT COUNT(*) FROM student WHERE student.semster = semster.ID) ,(SELECT COUNT(*) FROM courses WHERE courses.semster = semster.ID)
            FROM semster
            '''
    cursor.execute(query)
    results = cursor.fetchall()
    return results

def remove_semster_func(ID):
    query =\
        f'''DELETE FROM semster WHERE ID = {ID}
            '''
    cursor.execute(query)
    conn.commit()

def add_semster(name):
    query =\
        f'''INSERT INTO semster VALUES ('{name}')'''
    cursor.execute(query)
    conn.commit()

def get_semster(ID):
    query =\
        f'''SELECT * FROM semster WHERE ID = {ID}
            '''
    cursor.execute(query)
    results = cursor.fetchone()
    return results

def save_semster(ID, name):
    query =\
        f'''UPDATE semster SET semester_name='{name}' WHERE ID = {ID}
            '''
    cursor.execute(query)
    conn.commit()

    return True

@app.route('/semsters')
def semsters_page():
    semsters = get_semsters()
    return render_template('semsters.html', semsters = semsters)

@app.route('/remove_semster', methods=['GET'])
def remove_semster_req():
    if request.method == 'GET':
        ID = request.args.get('ID')
        remove_semster_func(ID)
        return redirect('/semsters')

@app.route('/add_semster', methods=['POST'])
def add_semster_req():
    if request.method == 'POST':
        semester_name = request.form['semster_name']

        save = add_semster(semester_name)
        return redirect('/semsters')

@app.route('/edit_semster_page', methods=['GET'])
def edit_semster_req():
    if request.method == 'GET':
        ID = request.args.get('ID')
        semster = get_semster(ID)
        ret = request.args.get('ret')
        return render_template('edit-semster.html', semster = semster, ret= ret)

@app.route('/edit_semster', methods=['POST'])
def edit_semster():
    if request.method == 'POST':
        ID = request.form['id']
        name = request.form['semster_name']

        save = save_semster(ID, name)
        return redirect(f'''/edit_semster_page?ID={ID}&ret={save}''')

# Courses

def remove_course_func(ID):
    query =\
        f'''DELETE FROM courses WHERE ID = {ID}
            '''
    cursor.execute(query)
    conn.commit()

def get_courses():
    query =\
        f'''SELECT courses.ID, courses.course_name, (SELECT semster.semester_name FROM semster WHERE semster.ID = courses.semster), (SELECT doctors.doctor_name FROM doctors WHERE doctors.NID = courses.doctor), (SELECT COUNT(*) FROM student WHERE student.semster = courses.semster)
            FROM courses
            '''
    cursor.execute(query)
    results = cursor.fetchall()
    return results

def add_course(name, semster, doctor):
    query =\
        f'''INSERT INTO courses VALUES ('{name}', {semster}, {doctor})'''
    cursor.execute(query)
    conn.commit()

def get_course(ID):
    query =\
        f'''SELECT * FROM courses WHERE ID = {ID}
            '''
    cursor.execute(query)
    results = cursor.fetchone()
    return results

def save_course(ID, name, semster, doctor):
    query =\
        f'''UPDATE courses SET course_name='{name}', semster = {semster}, doctor = {doctor} WHERE ID = {ID}
            '''
    cursor.execute(query)
    conn.commit()

    return True

@app.route('/courses')
def courses_page():
    courses = get_courses()
    return render_template('courses.html', courses = courses, doctors = get_doctors(), semsters = get_semsters())

@app.route('/remove_course', methods=['GET'])
def remove_course_req():
    if request.method == 'GET':
        ID = request.args.get('ID')
        remove_course_func(ID)
        return redirect('/courses')
        
@app.route('/add_course', methods=['POST'])
def add_course_req():
    if request.method == 'POST':
        course_name = request.form['course_name']
        semster = request.form['semster']
        doctor = request.form['doctor']

        save = add_course(course_name, semster, doctor)
        return redirect('/courses')

@app.route('/edit_course_page', methods=['GET'])
def edit_course_req():
    if request.method == 'GET':
        ID = request.args.get('ID')
        course = get_course(ID)
        ret = request.args.get('ret')
        return render_template('edit_course_page.html', course = course,  doctors = get_doctors(), semsters = get_semsters(), ret= ret)

@app.route('/edit_course', methods=['POST'])
def edit_course():
    if request.method == 'POST':
        ID = request.form['id']
        name = request.form['course_name']
        semster = request.form['semster']
        doctor = request.form['doctor']

        save = save_course(ID, name, semster, doctor)
        return redirect(f'''/edit_course_page?ID={ID}&ret={save}''')

# OUR NAMES
@app.route('/Team')
def Team():
    return render_template('Team.html')

app.run(debug=True)
# Close the cursor and connection
cursor.close()
conn.close()