"""
预排课系统数据库操作模块
功能：
1. 提供数据库连接和基本操作
2. 实现用户认证相关的数据库操作
3. 处理课程信息的数据库CRUD操作
4. 管理教师信息的数据库查询
5. 提供历史课程数据的查询功能

依赖：
- MySQL Connector/Python
- python-dotenv
- flask-bcrypt
"""

import mysql.connector
from mysql.connector import Error
from flask_bcrypt import Bcrypt
from dotenv import load_dotenv
import os
from utils import parse_teacher_name_and_headcount, split_teachers

# SQL查询常量
# 用户相关查询
SQL_GET_USER = "SELECT * FROM user_info WHERE account = %s"
SQL_UPDATE_PASSWORD = "UPDATE user_info SET password = %s WHERE account = %s"
SQL_INCREMENT_LOGIN_ATTEMPTS = """
    UPDATE user_info 
    SET 
        login_attempts = login_attempts + 1,
        lock_until = CASE 
            WHEN login_attempts + 1 >= 5 THEN UTC_TIMESTAMP() + INTERVAL 10 MINUTE 
            ELSE lock_until 
        END
    WHERE account = %s;
"""
SQL_GET_LOGIN_ATTEMPTS = "SELECT login_attempts, lock_until FROM user_info WHERE account = %s"
SQL_RESET_LOGIN_ATTEMPTS = "UPDATE user_info SET login_attempts = 0, lock_until = NULL WHERE account = %s"

# 课程相关查询
SQL_CHECK_COURSE = "SELECT * FROM 本学年课程信息 WHERE 学年学期 = %s AND 课程名称 = %s AND 教师姓名 = %s"
SQL_UPDATE_COURSE = """
    UPDATE 本学年课程信息
    SET 学生人数 = 学生人数 + %s, 总头数 = %s
    WHERE 学年学期 = %s AND 课程名称 = %s AND 教师姓名 = %s;
"""
SQL_INSERT_COURSE = """
    INSERT INTO 本学年课程信息 (学年学期, 课程名称, 教师姓名, 学时, 学生人数, 总头数)
    VALUES (%s, %s, %s, %s, %s, %s);
"""
SQL_DELETE_COURSE = "DELETE FROM 本学年课程信息 WHERE 课程名称 = %s"

# 教师相关查询
SQL_GET_TEACHERS = """
    SELECT 姓名 FROM 教师信息 
    WHERE 序号 >= 1 AND 备注 != %s;
"""

# 历史课程查询
SQL_GET_ALL_SEMESTERS = "SELECT DISTINCT 学年学期 FROM 历史课表 ORDER BY 学年学期 ASC"

# 表创建语句
SQL_CREATE_CURRENT_YEAR_TABLE = """
    CREATE TABLE IF NOT EXISTS 本学年课程信息 (
        学年学期 VARCHAR(5),
        课程名称 VARCHAR(30),  
        教师姓名 VARCHAR(10),   
        学时 INT,
        头数 INT DEFAULT 0,
        学生人数 INT DEFAULT 0,
        总头数 INT DEFAULT 0,
        PRIMARY KEY (学年学期, 课程名称, 教师姓名)
    );
"""

# 加载.env 文件
load_dotenv()

# 读取环境变量中的数据库配置
db_config = {
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'host': os.getenv('DB_HOST'),
    'database': os.getenv('DB_DATABASE')
}

# 初始化 Bcrypt（将在app.py中重新配置）
bcrypt = None

def init_bcrypt(app):
    """初始化Bcrypt用于密码加密"""
    global bcrypt
    bcrypt = Bcrypt(app)

def connect_to_db():
    """建立与MySQL数据库的连接并返回连接对象"""
    try:
        cnx = mysql.connector.connect(**db_config)
        return cnx
    except Error as e:
        print(f"Error connecting to database: {e}")
        return None

def get_user_by_account(account):
    """根据账号获取用户信息
    
    参数:
        account (str): 用户账号
        
    返回:
        dict: 用户信息字典，如果未找到则返回None
    """
    cnx = connect_to_db()
    if not cnx:
        return None
    cursor = cnx.cursor(dictionary=True)
    query = SQL_GET_USER
    cursor.execute(query, (account,))
    user = cursor.fetchone()
    cursor.close()
    cnx.close()
    return user


def verify_password(hashed_password, password):
    """验证密码是否匹配
    
    参数:
        hashed_password (str): 数据库中存储的哈希密码
        password (str): 用户输入的明文密码
        
    返回:
        bool: 密码是否匹配
    """
    return bcrypt.check_password_hash(hashed_password, password)


def update_user_password(account, new_password):
    """更新用户密码
    
    参数:
        account (str): 用户账号
        new_password (str): 新密码
        
    返回:
        bool: 更新是否成功
    """
    cnx = connect_to_db()
    if not cnx:
        return False
    cursor = cnx.cursor()
    hashed_password = bcrypt.generate_password_hash(new_password).decode('utf-8')
    query = SQL_UPDATE_PASSWORD
    cursor.execute(query, (hashed_password, account))
    cnx.commit()
    cursor.close()
    cnx.close()
    return True


def increment_failed_attempts(account):
    """增加登录失败次数并检查是否冻结账号
    
    参数:
        account (str): 用户账号
        
    返回:
        tuple: (失败次数, 锁定时间)
    """
    cnx = connect_to_db()
    if not cnx:
        return None, None
    cursor = cnx.cursor(dictionary=True)
    try:
        update_query = SQL_INCREMENT_LOGIN_ATTEMPTS
        cursor.execute(update_query, (account,))
        cnx.commit()

        select_query = SQL_GET_LOGIN_ATTEMPTS
        cursor.execute(select_query, (account,))
        result = cursor.fetchone()
        cursor.close()
        cnx.close()
        if result:
            return result['login_attempts'], result['lock_until']
        return None, None
    except Error as e:
        print(f"Error incrementing failed attempts: {e}")
        cursor.close()
        cnx.close()
        return None, None


def reset_login_attempts(account):
    """重置用户登录失败次数和锁定时间
    
    参数:
        account (str): 用户账号
        
    返回:
        bool: 重置是否成功
    """
    cnx = connect_to_db()
    if not cnx:
        return False
    cursor = cnx.cursor()
    try:
        update_query = SQL_RESET_LOGIN_ATTEMPTS
        cursor.execute(update_query, (account,))
        cnx.commit()
        cursor.close()
        cnx.close()
        return True
    except Error as e:
        print(f"Error resetting login attempts: {e}")
        cursor.close()
        cnx.close()
        return False


def check_existing_records(course_name, semester):
    """检查是否存在相同课程名称和学期的记录
    
    参数:
        course_name (str): 课程名称
        semester (str): 学年学期
        
    返回:
        list: 匹配的记录列表
    """
    cnx = connect_to_db()
    if not cnx:
        return None
    cursor = cnx.cursor()
    check_query = """
    SELECT * FROM 本学年课程信息 
    WHERE 课程名称 = %s AND 学年学期 = %s;
    """
    params = (course_name, semester)
    try:
        cursor.execute(check_query, params)
        results = cursor.fetchall()
        cursor.close()
        cnx.close()
        return results
    except Error as e:
        print(f"Error checking existing records: {e}")
        cursor.close()
        cnx.close()
        return None

def get_teacher_names():
    """获取所有教师姓名列表（除校领导外）
    
    返回:
        list: 教师姓名列表
    """
    cnx = connect_to_db()
    if not cnx:
        return None
    cursor = cnx.cursor()
    query = SQL_GET_TEACHERS
    params = ('校领导',)
    try:
        cursor.execute(query, params)
        results = cursor.fetchall()
        cursor.close()
        cnx.close()
        return results
    except Error as e:
        print(f"Error fetching data from database: {e}")
        cursor.close()
        cnx.close()
        return None

def delete_old_records(old_course_name, old_semester, old_teachers_array, old_total_head):
    """删除旧的课程记录
    
    参数:
        old_course_name (str): 课程名称
        old_semester (str): 学年学期
        old_teachers_array (list): 教师数组
        old_total_head (int): 总头数
        
    返回:
        bool: 删除是否成功
    """
    cnx = connect_to_db()
    if not cnx:
        print("无法连接到数据库")
        return False

    cursor = cnx.cursor()

    # 将教师姓名数组转换为列表
    teachers_list = split_teachers(old_teachers_array)

    for teacher in teachers_list:
        full_teacher_name, _, _ = parse_teacher_name_and_headcount(teacher)

        # 使用精确匹配来处理教师姓名、总头数和学年学期
        delete_query = """
        DELETE FROM 本学年课程信息 
        WHERE 课程名称 = %s AND 学年学期 = %s AND 教师姓名 = %s AND 总头数 = %s;
        """
        params = (old_course_name, old_semester, full_teacher_name, old_total_head)

        try:
            cursor.execute(delete_query, params)
            if cursor.rowcount == 0:
                print(
                    f"没有找到要删除的记录: 课程名称={old_course_name}, 学期={old_semester}, 教师姓名={full_teacher_name}, 总头数={old_total_head}")
            else:
                print(
                    f"成功删除记录: 课程名称={old_course_name}, 学期={old_semester}, 教师姓名={full_teacher_name}, 总头数={old_total_head}")
        except Error as e:
            print(
                f"删除记录时发生错误: 课程名称={old_course_name}, 学期={old_semester}, 教师姓名={full_teacher_name} - 错误信息: {e}")
            cursor.close()
            cnx.close()
            return False

    cnx.commit()
    cursor.close()
    cnx.close()
    return True


def add_new_records(new_course_name, new_hours, new_students, new_total_head, new_semester, new_teachers_array):
    """添加新的课程记录
    
    参数:
        new_course_name (str): 课程名称
        new_hours (int): 课程学时
        new_students (int): 学生人数
        new_total_head (int): 总头数
        new_semester (str): 学年学期
        new_teachers_array (list): 教师数组
        
    返回:
        dict: 包含操作状态和数据的响应
    """
    cnx = connect_to_db()
    if not cnx:
        print("无法连接到数据库")
        return {"status": 50000, "info": "数据库连接失败", "data": []}

    cursor = cnx.cursor()

    response_data = []

    # 将教师姓名数组转换为列表
    teachers_list = split_teachers(new_teachers_array)

    for teacher in teachers_list:
        full_teacher_name, _, headcount = parse_teacher_name_and_headcount(teacher)

        insert_query = SQL_INSERT_COURSE
        params = (new_semester, new_course_name, full_teacher_name, new_hours, headcount, new_students, new_total_head)

        try:
            cursor.execute(insert_query, params)
            # 构建每个记录的字典并添加到 response_data 列表中
            record = {
                "course_name": new_course_name,
                "hours": new_hours,
                "semester": new_semester,
                "teacher": full_teacher_name,
                "heads": headcount,
                "students": new_students,
                "total_head": new_total_head
            }
            response_data.append(record)  # 记录成功的教师及其相关信息
            print(
                f"成功插入记录: 课程名称={new_course_name}, 学期={new_semester}, 教师姓名={full_teacher_name}, 头数={headcount}, 总头数={new_total_head}")
        except Error as e:
            print(
                f"插入记录时发生错误: 课程名称={new_course_name}, 学期={new_semester}, 教师姓名={full_teacher_name} - 错误信息: {e}")
            cursor.close()
            cnx.close()
            return {"status": 50000, "info": "操作失败", "data": []}

    cnx.commit()
    cursor.close()
    cnx.close()

    response = {
        "status": 10000,
        "info": "success",
        "data": response_data  # 确保 data 是一个包含字典的列表
    }

    return response

def create_current_year_table_if_not_exists():
    """创建本学年课程信息表（如果不存在）
    
    注意: 此函数应在应用启动时调用一次，而不是每次操作前都调用
    
    返回:
        bool: 创建是否成功
    """
    cnx = connect_to_db()
    if not cnx:
        return False
    cursor = cnx.cursor()
    create_table_query = SQL_CREATE_CURRENT_YEAR_TABLE
    try:
        cursor.execute(create_table_query)
        cnx.commit()
        cursor.close()
        cnx.close()
        return True
    except Error as e:
        print(f"Error creating table: {e}")
        cursor.close()
        cnx.close()
        return False


def add_or_update_course(course_name, hours, students, semester, teacher, total_head):
    """添加或更新课程信息
    
    参数:
        course_name (str): 课程名称
        hours (int): 课程学时
        students (int): 学生人数
        semester (str): 学年学期
        teacher (str): 教师姓名
        total_head (int): 总头数
        
    返回:
        dict: 包含操作状态和数据的响应
    """
    cnx = connect_to_db()
    if not cnx:
        return {"status": 50000, "info": "数据库连接失败", "data": {}}
    cursor = cnx.cursor()
    check_query = SQL_CHECK_COURSE
    cursor.execute(check_query, (semester, course_name, teacher))
    existing_record = cursor.fetchone()
    if existing_record:
        update_query = SQL_UPDATE_COURSE
        params = (students, total_head, semester, course_name, teacher)
        operation_type = "updated"
    else:
        insert_query = SQL_INSERT_COURSE
        params = (semester, course_name, teacher, hours, students, total_head)
        operation_type = "inserted"
    try:
        cursor.execute(update_query if existing_record else insert_query, params)
        cnx.commit()
        cursor.close()
        cnx.close()
        response = {
            "status": 10000,
            "info": f"{operation_type} success",
            "data": {
                "course_name": course_name,
                "hours": hours,
                "students": students,
                "semester": semester,
                "teacher": teacher,
                "total_head": total_head
            }
        }
        return response
    except Error as e:
        print(f"Error inserting or updating data into database: {e}")
        cursor.close()
        cnx.close()
        return {"status": 50000, "info": "操作失败", "data": {}}


def get_courses(request):
    """获取课程列表，支持按学期和教师筛选
    
    参数:
        request: Flask请求对象
        
    返回:
        dict: 包含课程列表的响应
    """
    semester = request.args.get('semester')
    teacher = request.args.get('teacher')
    cnx = connect_to_db()
    if not cnx:
        return {"status": 50000, "info": "数据库连接失败", "data": []}
    cursor = cnx.cursor(dictionary=True)
    query = "SELECT * FROM 本学年课程信息"
    conditions = []
    params = []
    if semester:
        conditions.append("学年学期 = %s")
        params.append(semester)
    if teacher:
        conditions.append("教师姓名 LIKE %s")
        params.append(f"%{teacher}%")
    if conditions:
        query += " WHERE " + " AND ".join(conditions)
    try:
        cursor.execute(query, tuple(params))
        rows = cursor.fetchall()
        cursor.close()
        cnx.close()
        if rows:
            response = {
                "status": 10000,
                "info": "success",
                "data": [
                    {
                        "course_name": row.get('课程名称', ''),
                        "hours": row.get('学时', 0),
                        "semester": row.get('学年学期', ''),
                        "teacher": row.get('教师姓名', ''),
                        "heads": row.get('头数', 0),
                        "students": row.get('学生人数', ''),
                        "total_head": row.get('总头数', ''),
                    }
                    for row in rows
                ]
            }
        else:
            response = {
                "status": 40401,
                "info": f"{semester}课程不存在",
                "data": []
            }
        return response
    except Error as e:
        print(f"Error querying data from database: {e}")
        cursor.close()
        cnx.close()
        return {"status": 50000, "info": "查询失败", "data": []}


def get_all_semesters_from_db():
    """获取历史课表中所有学期列表
    
    返回:
        list: 学期字符串列表
    """
    cnx = connect_to_db()
    if not cnx:
        return []
    cursor = cnx.cursor()
    query = SQL_GET_ALL_SEMESTERS
    try:
        cursor.execute(query)
        results = cursor.fetchall()
        cursor.close()
        cnx.close()
        return [row[0] for row in results]
    except Error as e:
        print(f"Error fetching semesters from database: {e}")
        cursor.close()
        cnx.close()
        return []


def query_history_courses(semester=None, teacher=None):
    """查询历史课程信息，支持按学期和教师筛选
    
    参数:
        semester (str, optional): 学年学期
        teacher (str, optional): 教师姓名
        
    返回:
        dict: 包含历史课程列表的响应
    """
    cnx = connect_to_db()
    if not cnx:
        return {"status": 50000, "info": "数据库连接失败", "data": []}
    cursor = cnx.cursor(dictionary=True)
    all_semesters = get_all_semesters_from_db()
    if semester and semester not in all_semesters:
        return {"status": 40402, "info": "历史统计起始学期不存在", "data": []}
    if semester:
        target_semesters = [s for s in all_semesters if s >= semester]
    else:
        return {
            "status": 40402,
            "info": f"未找到历史课程数据",
            "data": []
        }
    conditions = []
    params = []
    if target_semesters:
        conditions.append("学年学期 IN (%s)" % ','.join(['%s'] * len(target_semesters)))
        params.extend(target_semesters)
    if teacher:
        conditions.append("任课教师 LIKE %s")
        params.append(f"%{teacher}%")
    query = "SELECT * FROM 历史课表"
    if conditions:
        query += " WHERE " + " AND ".join(conditions)
    try:
        cursor.execute(query, tuple(params))
        rows = cursor.fetchall()
        cursor.close()
        cnx.close()
        if rows:
            response = {
                "status": 10000,
                "info": "success",
                "data": [
                    {
                        "course_name": row.get('课程名称', ''),
                        "semester": row.get('学年学期', ''),
                        "teacher": row.get('任课教师', '')
                    }
                    for row in rows
                ]
            }
        else:
            response = {
                "status": 40401,
                "info": f"{semester}课程不存在",
                "data": []
            }
        return response
    except Error as e:
        print(f"Error querying data from database: {e}")
        cursor.close()
        cnx.close()
        return {"status": 50000, "info": "查询失败", "data": []}


def delete_course(course_name):
    """根据课程名称删除课程
    
    参数:
        course_name (str): 课程名称
        
    返回:
        dict: 操作结果响应
    """
    cnx = connect_to_db()
    if not cnx:
        return {"status": 50000, "info": "数据库连接失败"}
    cursor = cnx.cursor()
    delete_query = SQL_DELETE_COURSE
    params = (course_name,)
    try:
        cursor.execute(delete_query, params)
        cnx.commit()
        cursor.close()
        cnx.close()
        response = {
            "status": 10000,
            "info": "success"
        }
        return response
    except Error as e:
        print(f"Error deleting data from database: {e}")
        cursor.close()
        cnx.close()
        return {"status": 50000, "info": "删除失败"}
