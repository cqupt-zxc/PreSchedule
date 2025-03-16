"""
预排课系统后端主应用文件
功能：
1. 提供所有Web API接口
2. 处理用户认证和授权
3. 管理课程信息的增删改查
4. 处理教师信息查询
5. 提供历史课程查询功能
"""

from flask import Flask, request, jsonify
from database import add_or_update_course, get_courses, query_history_courses, delete_course, \
    create_current_year_table_if_not_exists, delete_old_records, \
    add_new_records, get_teacher_names, get_user_by_account, verify_password, increment_failed_attempts, \
    reset_login_attempts, update_user_password, init_bcrypt
from auth import verify_token, generate_token, get_current_user_from_token, is_admin
from datetime import datetime
from utils import clean_teacher_name, parse_teacher_name_and_headcount, split_teachers
import jwt
from dotenv import load_dotenv
import os
from functools import wraps
from logger import get_logger

# 获取日志记录器
logger = get_logger()

# 加载.env文件中的环境变量
load_dotenv()

app = Flask(__name__)
# 从环境变量中获取SECRET_KEY
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

# 初始化 Bcrypt
init_bcrypt(app)

# 确保应用启动时创建表
create_current_year_table_if_not_exists()

def handle_error(error_msg, status_code=400):
    """统一的错误处理函数"""
    logger.error(f"Error: {error_msg}, Status Code: {status_code}")
    return jsonify({"status": status_code, "info": error_msg}), status_code

def require_auth(f):
    """认证装饰器"""
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return handle_error("未登录或无效的token", 401)
        
        token = auth_header.split(' ')[1]
        try:
            payload = verify_token(token, app.config['SECRET_KEY'])
            if not payload:
                return handle_error("未登录或无效的token", 401)
            return f(*args, **kwargs)
        except jwt.ExpiredSignatureError:
            return handle_error("Token已过期", 401)
        except jwt.InvalidTokenError:
            return handle_error("无效的Token", 401)
    return decorated

def require_admin(f):
    """管理员权限装饰器"""
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return handle_error("未登录或无效的token", 401)
        
        token = auth_header.split(' ')[1]
        try:
            payload = verify_token(token, app.config['SECRET_KEY'])
            if not payload:
                return handle_error("未登录或无效的token", 401)
            if payload.get("role") != "admin":
                return handle_error("权限不足，管理员才能执行此操作", 403)
            return f(*args, **kwargs)
        except jwt.ExpiredSignatureError:
            return handle_error("Token已过期", 401)
        except jwt.InvalidTokenError:
            return handle_error("无效的Token", 401)
    return decorated

# 全局错误处理
@app.errorhandler(400)
def bad_request(error):
    return handle_error("请求参数错误", 400)

@app.errorhandler(401)
def unauthorized(error):
    return handle_error("未授权访问", 401)

@app.errorhandler(403)
def forbidden(error):
    return handle_error("禁止访问", 403)

@app.errorhandler(404)
def not_found(error):
    return handle_error("资源不存在", 404)

@app.errorhandler(500)
def internal_server_error(error):
    return handle_error("服务器内部错误", 500)

# 登录接口
@app.route("/admin/login", methods=["POST"])
def login():
    logger.info("Attempting login")
    req_data = request.get_json() or {}
    account = req_data.get("account")
    password = req_data.get("password")

    # 验证输入参数
    if not account or not isinstance(account, str) or len(account) < 1 or len(account) > 10:
        logger.warning(f"Invalid account format: {account}")
        return handle_error("用户名不能为空或长度超出范围", 400)
    if not password or not isinstance(password, str) or len(password) < 6 or len(password) > 15:
        logger.warning(f"Invalid password format for account: {account}")
        return handle_error("密码不能为空或长度超出范围", 400)

    user = get_user_by_account(account)
    if not user:
        logger.warning(f"Login attempt with non-existent account: {account}")
        return handle_error("用户名不存在", 401)

    # 检查账号是否被冻结
    current_time = datetime.utcnow()
    if user.get('lock_until') and user['lock_until'] > current_time:
        logger.warning(f"Account locked: {account}")
        return handle_error("账号已冻结，请10分钟后再试", 403)

    # 验证密码
    if not verify_password(user['password'], password):
        new_attempts, new_lock_until = increment_failed_attempts(account)
        if new_attempts is None:
            logger.error(f"Failed to increment login attempts for account: {account}")
            return handle_error("内部服务器错误", 500)

        if new_attempts >= 5 and new_lock_until and new_lock_until > current_time:
            logger.warning(f"Account locked due to too many failed attempts: {account}")
            return handle_error("密码错误次数过多，账号已冻结10分钟", 401)
        else:
            remaining = 5 - new_attempts
            logger.warning(f"Failed login attempt for account: {account}, remaining attempts: {remaining}")
            return handle_error(f"密码错误，剩余尝试次数：{remaining}", 401)

    # 登录成功，重置失败次数
    reset_login_attempts(account)
    token = generate_token(user['account'], user['id'], user['role'], expires_days=7)
    logger.info(f"Successful login for account: {account}")

    return jsonify({
        "status": 10000,
        "data": {
            "token": token,
            "account": user['account'],
            "role": user['role']
        },
        "info": "success"
    }), 200


# 修改密码接口
@app.route("/admin/fixpwd", methods=["POST"])
def fixpwd():
    req_data = request.get_json() or {}
    old_password = req_data.get("old_password")
    new_password = req_data.get("new_password")

    # 获取当前登录用户的信息（从 token 获取）
    current_user = get_current_user_from_token()
    if not current_user:
        return jsonify({"status": 401, "info": "未登录或无效的token"}), 401

    # 获取当前用户的账号和角色
    account = current_user["account"]
    role = current_user["role"]

    # 如果是普通用户，只能修改自己的密码，管理员可以修改任何人的密码
    if role != 'admin' and account != req_data.get("account"):
        return jsonify({"status": 40300, "info": "权限不足，普通用户只能修改自己的密码"}), 403

    # 验证密码长度
    if not old_password or not isinstance(old_password, str) or len(old_password) < 6 or len(old_password) > 15:
        return jsonify({"status": 40000, "info": "旧密码不能为空或长度超出范围"}), 400
    if not new_password or not isinstance(new_password, str) or len(new_password) < 6 or len(new_password) > 15:
        return jsonify({"status": 40000, "info": "新密码不能为空或长度超出范围"}), 400

    user = get_user_by_account(account)
    if not user:
        return jsonify({"status": 40400, "info": "用户不存在，无法修改密码"}), 404

    # 验证旧密码
    if not verify_password(user['password'], old_password):
        return jsonify({"status": 40102, "info": "原密码错误"}), 400

    # 更新密码
    success = update_user_password(account, new_password)
    if not success:
        return jsonify({"status": 40103, "info": "修改密码失败"}), 400

    return jsonify({"status": 10000, "info": "success"}), 200


@app.route('/teacher', methods=['GET'])
def get_teacher():
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return jsonify({"status": 401, "info": "未登录或无效的token"}), 401

    token = auth_header.split(' ')[1]
    if not verify_token(token, app.config['SECRET_KEY']):
        return jsonify({"status": 401, "info": "未登录或无效的token"}), 401

    results = get_teacher_names()
    if results is None:
        return jsonify({"status": 50000, "info": "数据库连接失败"}), 500

    # 清理教师姓名
    teacher_names = [clean_teacher_name(row[0]) for row in results]

    response = {
        "status": 10000,
        "info": "success",
        "data": [
            {
                "teacher": teacher_names
            }
        ]
    }
    return jsonify(response), 200


@app.route('/courses', methods=['POST'])
def add_course():
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return jsonify({"status": 401, "info": "未登录或无效的token"}), 401
    token = auth_header.split(' ')[1]
    try:
        current_user, current_user_role = get_current_user_from_token(token, app.config['SECRET_KEY'])
    except jwt.InvalidTokenError:
        return jsonify({"status": 401, "info": "无效的Token"}), 401

    if current_user_role != 'admin':
        return jsonify({"status": 403, "info": "权限不足，管理员才能执行此操作"}), 403

    data = request.json
    course_name = data.get('course_name')
    hours = data.get('hours')
    students = data.get('students')
    semester = data.get('semester')
    teacher = data.get('teacher', '无')
    total_head = data.get('total_head', 1)

    result = add_or_update_course(
        course_name=course_name,
        hours=hours,
        students=students,
        semester=semester,
        teacher=teacher,
        total_head=total_head
    )
    return jsonify(result)


@app.route('/courses', methods=['PUT'])
def update_course():
    """更新课程API
    
    管理员用户可以更新现有课程信息
    此API先删除旧记录，再添加新记录，实现课程信息的更新
    
    请求示例:
    {
        "old_course_name": "数据库原理",
        "old_hours": 48,
        "old_students": 60,
        "old_total_head": 1,
        "old_semester": "20242",
        "old_teachers": "张三",
        "new_course_name": "数据库原理与应用",
        "new_hours": 64,
        "new_students": 80,
        "new_total_head": 2,
        "new_semester": "20242",
        "new_teachers": "张三,李四"
    }
    """
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return jsonify({"status": 401, "info": "未登录或无效的token"}), 401
    token = auth_header.split(' ')[1]
    try:
        current_user, current_user_role = get_current_user_from_token(token, app.config['SECRET_KEY'])
    except jwt.InvalidTokenError:
        return jsonify({"status": 401, "info": "无效的Token"}), 401

    if current_user_role != 'admin':
        return jsonify({"status": 403, "info": "权限不足，管理员才能执行此操作"}), 403

    data = request.get_json()
    old_course_name = data.get('old_course_name')
    old_hours = data.get('old_hours')
    old_students = data.get('old_students')
    old_total_head = data.get('old_total_head')
    old_semester = data.get('old_semester')
    old_teachers_str = data.get('old_teachers', '')
    new_course_name = data.get('new_course_name')
    new_hours = data.get('new_hours')
    new_students = data.get('new_students')
    new_total_head = data.get('new_total_head')
    new_semester = data.get('new_semester')
    new_teachers_str = data.get('new_teachers', '')
    
    # 先删除旧记录
    delete_result = delete_old_records(old_course_name, old_semester, old_teachers_str, old_total_head)
    
    if not delete_result:
        return jsonify({
            "status": 50000,
            "info": "删除旧记录失败",
            "data": []
        })
    
    # 再添加新记录
    add_result = add_new_records(
        new_course_name=new_course_name,
        new_hours=new_hours,
        new_students=new_students,
        new_total_head=new_total_head,
        new_semester=new_semester,
        new_teachers_array=new_teachers_str
    )
    return jsonify(add_result)


@app.route('/courses', methods=['GET'])
def get_courses_route():
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return jsonify({"status": 401, "info": "未登录或无效的token"}), 401
    token = auth_header.split(' ')[1]
    if not verify_token(token, app.config['SECRET_KEY']):
        return jsonify({"status": 401, "info": "未登录或无效的token"}), 401
    result = get_courses(request)
    return jsonify(result)


@app.route('/history_courses', methods=['GET'])
def get_history_courses():
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return jsonify({"status": 401, "info": "未登录或无效的token"}), 401
    token = auth_header.split(' ')[1]
    if not verify_token(token, app.config['SECRET_KEY']):
        return jsonify({"status": 401, "info": "未登录或无效的token"}), 401
    semester = request.args.get('semester')
    teacher = request.args.get('teacher')
    result = query_history_courses(semester=semester, teacher=teacher)
    return jsonify(result)


@app.route('/courses', methods=['DELETE'])
def delete_course_route():
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return jsonify({"status": 40100, "info": "未提供或无效的Token", "data": {}}), 401
    token = auth_header.split(' ')[1]
    try:
        payload = verify_token(token, app.config['SECRET_KEY'])
        current_user_role = payload.get("role")
    except Exception:
        return jsonify({"status": 40100, "info": "未登录或无效的token", "data": {}}), 401
    if current_user_role != 'admin':
        return jsonify({"status": 40300, "info": "权限不足，管理员才能执行此操作", "data": {}}), 403
    course_name = request.args.get('course_name')
    if not course_name:
        return jsonify({"status": 40000, "info": "缺少必要参数"}), 400
    result = delete_course(course_name)
    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True)