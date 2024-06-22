from flask import Flask, request, jsonify, render_template, redirect, url_for, session
import pymysql
from pymysql.cursors import DictCursor
import bcrypt
import os
from dotenv import load_dotenv

# 加载 .env 文件中的环境变量
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')  # 用于会话管理

def get_db_connection():
    return pymysql.connect(
        host=os.getenv('DB_HOST'),
        user=os.getenv('DB_USER'),
        passwd=os.getenv('DB_PASS'),
        db=os.getenv('DB_NAME'),
        cursorclass=DictCursor
    )

@app.route('/')
def home():
    return render_template('login.html')






# 学生登录路由
@app.route('/login/student', methods=['GET', 'POST'])  
def student_login():
    if request.method == 'GET':
        return render_template('student_login.html')  # 渲染学生登录页面

    if request.method == 'POST':  # 处理 POST 请求
        conn = get_db_connection()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        try:
            data = request.get_json()
            if not data:
                app.logger.error("No JSON data received")
                return jsonify({"success": False, "message": "未收到请求数据"})

            student_id = data.get('studentId')
            password = data.get('password')
            if not student_id or not password:
                app.logger.error("Missing studentId or password")
                return jsonify({"success": False, "message": "学号或密码缺失"})

            # 查询密码表和角色信息
            query = "SELECT Role, Password FROM Passwords WHERE ID = %s AND Role = 'Student'"
            cursor.execute(query, (student_id,))
            result = cursor.fetchone()

            if result and password == result['Password']:
                # 登录成功，验证角色并设置会话
                session['student_id'] = student_id  # 设置会话
                return jsonify({"success": True, "student_id": student_id})  # 返回成功信息和学生ID
            else:
                app.logger.debug("Invalid credentials")
                return jsonify({"success": False, "message": "学号或密码错误"})
        except Exception as e:
            app.logger.error(f"Error during login: {str(e)}")
            return jsonify({"success": False, "message": f"服务器错误，请稍后再试: {str(e)}"})
        finally:
            cursor.close()
            conn.close()

#获取学生成绩
def get_student_grades(student_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        # 查询学生成绩和对应的课程名称
        query = """
        SELECT Course.CourseName, Grade.GradeLevel
        FROM Grade
        JOIN Course ON Grade.CourseID = Course.CourseID
        WHERE Grade.StudentID = %s
        """
        cursor.execute(query, (student_id,))
        grades = cursor.fetchall()
    finally:
        cursor.close()
        conn.close()
    return grades

#获取学生课程
def get_student_courses(student_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        # 查询学生选修的课程信息，包括课程名称、课程学期、教师ID和课程描述
        query = """
        SELECT Course.CourseName, Course.CourseTerm, Course.TeacherID, Course.CourseDescription
        FROM Enrollment
        JOIN Course ON Enrollment.CourseID = Course.CourseID
        WHERE Enrollment.StudentID = %s
        """
        cursor.execute(query, (student_id,))
        courses = cursor.fetchall()
    finally:
        cursor.close()
        conn.close()
    return courses


# 获取学生信息
def get_student_info(student_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        # 查询学生的基本信息
        query = """
        SELECT StudentName, StudentGender, StudentID, StudentIDNumber, 
               StudentDormitory, StudentGrade, EarnedCredits, RequiredCredits, DepartmentID
        FROM Student
        WHERE StudentID = %s
        """
        cursor.execute(query, (student_id,))
        student_info = cursor.fetchone()
    finally:
        cursor.close()
        conn.close()
    return student_info

@app.route('/dashboard/student/<student_id>', methods=['GET'])  
def student_dashboard(student_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        # 获取学生的课程信息
        query_courses = """
        SELECT Course.CourseName, Course.CourseTerm, Course.TeacherID, Course.CourseDescription
        FROM Enrollment
        JOIN Course ON Enrollment.CourseID = Course.CourseID
        WHERE Enrollment.StudentID = %s
        """
        cursor.execute(query_courses, (student_id,))
        courses = cursor.fetchall()

        # 获取学生的成绩信息
        query_grades = """
        SELECT Course.CourseName, Grade.GradeLevel
        FROM Grade
        JOIN Course ON Grade.CourseID = Course.CourseID
        WHERE Grade.StudentID = %s
        """
        cursor.execute(query_grades, (student_id,))
        grades = cursor.fetchall()

        # 获取学生的基本信息
        student_info = get_student_info(student_id)

        # 渲染学生仪表板模板
        return render_template('student_dashboard.html', courses=courses, grades=grades, student_info=student_info)
    except Exception as e:
        app.logger.error(f"Error loading dashboard: {str(e)}")
        return f"An error occurred: {str(e)}"
    finally:
        cursor.close()
        conn.close()


@app.route('/change_password', methods=['POST'])
def change_password():
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        data = request.get_json()
        user_id = data.get('userId')
        role = data.get('role')
        current_password = data.get('currentPassword')
        new_password = data.get('newPassword')

        if not user_id or not role or not current_password or not new_password:
            return jsonify({"success": False, "message": "缺少必要的参数"})

        # 验证当前密码
        query = "SELECT Password FROM Passwords WHERE ID = %s AND Role = %s"
        cursor.execute(query, (user_id, role))
        result = cursor.fetchone()

        if not result or current_password != result['Password']:
            return jsonify({"success": False, "message": "当前密码不正确"})

        # 更新为新密码
        update_query = "UPDATE Passwords SET Password = %s WHERE ID = %s AND Role = %s"
        cursor.execute(update_query, (new_password, user_id, role))
        conn.commit()

        return jsonify({"success": True, "message": "密码更新成功"})
    except Exception as e:
        app.logger.error(f"Error changing password: {str(e)}")
        return jsonify({"success": False, "message": f"服务器错误，请稍后再试: {str(e)}"})
    finally:
        cursor.close()
        conn.close()









# 教师登录路由
@app.route('/login/teacher', methods=['GET', 'POST'])
def teacher_login():
    if request.method == 'GET':
        return render_template('teacher_login.html')  # 渲染教师登录页面

    if request.method == 'POST':  # 处理 POST 请求
        conn = get_db_connection()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        try:
            data = request.get_json()
            if not data:
                app.logger.error("No JSON data received")
                return jsonify({"success": False, "message": "未收到请求数据"})

            user_id = data.get('userId')
            password = data.get('password')
            if not user_id or not password:
                app.logger.error("Missing userId or password")
                return jsonify({"success": False, "message": "工号或密码缺失"})

            # 查询密码表和角色信息
            query = "SELECT Role, Password FROM Passwords WHERE ID = %s AND Role = 'Teacher'"
            cursor.execute(query, (user_id,))
            result = cursor.fetchone()

            if result and password == result['Password']:
                # 登录成功，验证角色并设置会话
                session['teacher_id'] = user_id  # 设置会话
                return jsonify({"success": True, "userId": user_id})  # 返回成功信息和用户ID
            else:
                app.logger.debug("Invalid credentials")
                return jsonify({"success": False, "message": "工号或密码错误"})
        except Exception as e:
            app.logger.error(f"Error during login: {str(e)}")
            return jsonify({"success": False, "message": f"服务器错误，请稍后再试: {str(e)}"})
        finally:
            cursor.close()
            conn.close()

@app.route('/record_grade', methods=['POST'])
def record_grade():
    if 'teacher_id' not in session:
        return jsonify({"success": False, "message": "用户未登录"})

    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        data = request.get_json()
        teacher_id = session['teacher_id']  # 从会话中获取教师ID
        grade_id = data.get('gradeId')
        student_id = data.get('studentId')
        course_id = data.get('courseId')
        grade_level = data.get('gradeLevel')
        record_time = data.get('recordTime')

        if not grade_id or not student_id or not course_id or not grade_level or not record_time:
            return jsonify({"success": False, "message": "缺少必要的参数"})

        # 插入成绩记录
        insert_grade_query = """
        INSERT INTO Grade (GradeID, CourseID, StudentID, GradeLevel)
        VALUES (%s, %s, %s, %s)
        """
        cursor.execute(insert_grade_query, (grade_id, course_id, student_id, grade_level))

        # 插入录入记录
        insert_record_query = """
        INSERT INTO Record (TeacherID, GradeID, RecordTime)
        VALUES (%s, %s, %s)
        """
        cursor.execute(insert_record_query, (teacher_id, grade_id, record_time))

        conn.commit()

        return jsonify({"success": True, "message": "成绩录入成功"})
    except Exception as e:
        app.logger.error(f"Error recording grade: {str(e)}")
        return jsonify({"success": False, "message": f"服务器错误，请稍后再试: {str(e)}"})
    finally:
        cursor.close()
        conn.close()


@app.route('/dashboard/teacher/<teacher_id>', methods=['GET'])
def teacher_dashboard(teacher_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        # 获取教师的课程信息
        query_courses = """
        SELECT Course.CourseID, Course.CourseName, Course.CourseTerm, Course.CourseDescription
        FROM Course
        WHERE Course.TeacherID = %s
        """
        cursor.execute(query_courses, (teacher_id,))
        courses = cursor.fetchall()
        app.logger.info(f"Courses fetched for teacher {teacher_id}")

        # 获取教师录入的成绩信息
        query_grades = """
        SELECT Grade.GradeID, Grade.StudentID, Student.StudentName, Course.CourseName, Grade.GradeLevel, Record.RecordTime
        FROM Grade
        JOIN Record ON Grade.GradeID = Record.GradeID
        JOIN Student ON Grade.StudentID = Student.StudentID
        JOIN Course ON Grade.CourseID = Course.CourseID
        WHERE Record.TeacherID = %s
        """
        cursor.execute(query_grades, (teacher_id,))
        grades = cursor.fetchall()
        app.logger.info(f"Grades fetched for teacher {teacher_id}")

        # 获取教师的基本信息
        query_teacher_info = """
        SELECT TeacherName, TeacherGender, TeacherID, DepartmentID, TeacherPhone, TeacherOffice
        FROM Teacher
        WHERE TeacherID = %s
        """
        cursor.execute(query_teacher_info, (teacher_id,))
        teacher_info = cursor.fetchone()
        app.logger.info(f"Teacher info fetched for teacher {teacher_id}")

        # 渲染教师仪表板模板
        return render_template('teacher_dashboard.html', courses=courses, grades=grades, teacher_info=teacher_info)
    except Exception as e:
        app.logger.error(f"Error loading dashboard for teacher {teacher_id}: {str(e)}")
        return f"An error occurred: {str(e)}"
    finally:
        cursor.close()
        conn.close()
        app.logger.info(f"Database connection closed for teacher {teacher_id}")





# 管理登录路由
@app.route('/login/admin', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'GET':
        return render_template('admin_login.html')  # 渲染管理员登录页面

    if request.method == 'POST':  # 处理 POST 请求
        conn = get_db_connection()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        try:
            data = request.get_json()
            if not data:
                app.logger.error("No JSON data received")
                return jsonify({"success": False, "message": "未收到请求数据"})

            admin_id = data.get('adminId')
            password = data.get('password')
            if not admin_id or not password:
                app.logger.error("Missing adminId or password")
                return jsonify({"success": False, "message": "工号或密码缺失"})

            # 查询密码表和角色信息
            query = "SELECT Role, Password FROM Passwords WHERE ID = %s AND (Role = 'Admin' OR Role = 'DepartmentHead')"
            cursor.execute(query, (admin_id,))
            result = cursor.fetchone()

            if result and password == result['Password']:
                # 登录成功，验证角色并设置会话
                session['admin_id'] = admin_id  # 设置会话
                return jsonify({"success": True, "admin_id": admin_id, "role": result['Role']})  # 返回成功信息、用户ID和角色
            else:
                app.logger.debug("Invalid credentials")
                return jsonify({"success": False, "message": "工号或密码错误"})
        except Exception as e:
            app.logger.error(f"Error during login: {str(e)}")
            return jsonify({"success": False, "message": f"服务器错误，请稍后再试: {str(e)}"})
        finally:
            cursor.close()
            conn.close()




            

# 管理员仪表板路由
@app.route('/dashboard/admin/<admin_id>', methods=['GET'])
def admin_dashboard(admin_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        # 获取管理员的基本信息
        query_admin_info = """
        SELECT AdminName, AdminGender, AdminID, AdminPhone, AdminOffice
        FROM DepartmentAdmin
        WHERE AdminID = %s
        """
        cursor.execute(query_admin_info, (admin_id,))
        admin_info = cursor.fetchone()

        # 获取院系信息
        query_departments = """
        SELECT DepartmentID, DepartmentName, DepartmentPhone, DepartmentOffice
        FROM Department
        """
        cursor.execute(query_departments)
        departments = cursor.fetchall()

        # 渲染管理员仪表板模板
        return render_template('department_administrator_dashboard.html', admin_info=admin_info, departments=departments)
    except Exception as e:
        app.logger.error(f"Error loading dashboard: {str(e)}")
        return f"An error occurred: {str(e)}"
    finally:
        cursor.close()
        conn.close()

# 获取院系详情
@app.route('/get_department_details', methods=['GET'])
def get_department_details():
    department_id = request.args.get('department_id')
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        query = """
        SELECT DepartmentID, DepartmentName, DepartmentPhone, DepartmentOffice
        FROM Department
        WHERE DepartmentID = %s
        """
        cursor.execute(query, (department_id,))
        department_details = cursor.fetchall()
        return jsonify({"departments": department_details})
    except Exception as e:
        app.logger.error(f"Error fetching department details: {str(e)}")
        return jsonify({"success": False, "message": f"服务器错误，请稍后再试: {str(e)}"})
    finally:
        cursor.close()
        conn.close()

# 更新院系信息
@app.route('/update_department', methods=['POST'])
def update_department():
    data = request.get_json()
    department_id = data.get('departmentID')
    new_phone = data.get('newPhone')
    new_office = data.get('newOffice')
    
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        query = """
        UPDATE Department
        SET DepartmentPhone = %s, DepartmentOffice = %s
        WHERE DepartmentID = %s
        """
        cursor.execute(query, (new_phone, new_office, department_id))
        conn.commit()
        return jsonify({"success": True, "message": "院系信息更新成功"})
    except Exception as e:
        app.logger.error(f"Error updating department: {str(e)}")
        return jsonify({"success": False, "message": f"服务器错误，请稍后再试: {str(e)}"})
    finally:
        cursor.close()
        conn.close()








# 院系主任仪表盘路由
@app.route('/dashboard/department_head/<head_id>', methods=['GET'])
def department_head_dashboard(head_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        # 获取院系主任的基本信息
        query_head_info = """
        SELECT HeadName AS name, HeadEmail AS email, HeadID, DepartmentID, HeadPhone AS phone, HeadOffice AS office
        FROM DepartmentHead
        WHERE HeadID = %s
        """
        cursor.execute(query_head_info, (head_id,))
        head_info = cursor.fetchone()

        # 获取教师信息
        query_teachers = """
        SELECT TeacherID AS teacher_id, TeacherName AS teacher_name, TeacherGender AS gender, TeacherPhone AS phone
        FROM Teacher
        WHERE DepartmentID = %s
        """
        cursor.execute(query_teachers, (head_info['DepartmentID'],))
        teachers = cursor.fetchall()

        # 获取院系信息
        query_department = """
        SELECT DepartmentName AS name, DepartmentID AS code, DepartmentPhone AS phone, DepartmentOffice AS location
        FROM Department
        WHERE DepartmentID = %s
        """
        cursor.execute(query_department, (head_info['DepartmentID'],))
        department = cursor.fetchone()

        # 渲染院系主任仪表板模板
        return render_template('department_head_dashboard.html', head=head_info, teachers=teachers, department=department)
    except Exception as e:
        app.logger.error(f"Error loading dashboard: {str(e)}")
        return f"An error occurred: {str(e)}"
    finally:
        cursor.close()
        conn.close()

# 获取教师详情
@app.route('/get_teacher_details', methods=['GET'])
def get_teacher_details():
    teacher_id = request.args.get('teacher_id')
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        query = """
        SELECT TeacherID AS teacher_id, TeacherName AS teacher_name, TeacherGender AS gender, TeacherPhone AS phone
        FROM Teacher
        WHERE TeacherID = %s
        """
        cursor.execute(query, (teacher_id,))
        teacher_details = cursor.fetchall()
        return jsonify({"teachers": teacher_details})
    except Exception as e:
        app.logger.error(f"Error fetching teacher details: {str(e)}")
        return jsonify({"success": False, "message": "获取教师详情失败"})
    finally:
        cursor.close()
        conn.close()

# 更新教师信息
@app.route('/update_teacher', methods=['POST'])
def update_teacher():
    data = request.get_json()
    teacher_id = data.get('teacherId')
    new_phone = data.get('newPhone')
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        query = """
        UPDATE Teacher
        SET TeacherPhone = %s
        WHERE TeacherID = %s
        """
        cursor.execute(query, (new_phone, teacher_id))
        conn.commit()
        return jsonify({"success": True, "message": "教师信息更新成功"})
    except Exception as e:
        app.logger.error(f"Error updating teacher information: {str(e)}")
        return jsonify({"success": False, "message": "教师信息更新失败"})
    finally:
        cursor.close()
        conn.close()












































if __name__ == '__main__':
    app.run(debug=True)
