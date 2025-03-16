"""
预排课系统数据验证模块
功能：
1. 提供请求数据的验证函数
2. 定义数据验证规则
3. 统一处理验证错误
"""

from datetime import datetime

def validate_login_data(data):
    """验证登录数据"""
    errors = []
    account = data.get('account')
    password = data.get('password')

    if not account:
        errors.append("用户名不能为空")
    elif not isinstance(account, str):
        errors.append("用户名必须是字符串")
    elif len(account) < 1 or len(account) > 10:
        errors.append("用户名长度必须在1-10个字符之间")

    if not password:
        errors.append("密码不能为空")
    elif not isinstance(password, str):
        errors.append("密码必须是字符串")
    elif len(password) < 6 or len(password) > 15:
        errors.append("密码长度必须在6-15个字符之间")

    return errors

def validate_course_data(data):
    """验证课程数据"""
    errors = []
    course_name = data.get('course_name')
    hours = data.get('hours')
    students = data.get('students')
    semester = data.get('semester')
    teacher = data.get('teacher')
    total_head = data.get('total_head')

    if not course_name:
        errors.append("课程名称不能为空")
    elif not isinstance(course_name, str):
        errors.append("课程名称必须是字符串")
    elif len(course_name) > 30:
        errors.append("课程名称不能超过30个字符")

    if not isinstance(hours, (int, float)) or hours <= 0:
        errors.append("学时必须是大于0的数字")

    if not isinstance(students, int) or students < 0:
        errors.append("学生人数必须是非负整数")

    if not semester:
        errors.append("学期不能为空")
    elif not isinstance(semester, str):
        errors.append("学期必须是字符串")
    elif len(semester) != 5:
        errors.append("学期格式错误（应为5位字符，如20241）")
    else:
        try:
            year = int(semester[:4])
            term = int(semester[4])
            current_year = datetime.now().year
            if year < 2000 or year > current_year + 1:
                errors.append("年份不合理")
            if term not in [1, 2]:
                errors.append("学期只能是1或2")
        except ValueError:
            errors.append("学期格式错误")

    if teacher and not isinstance(teacher, str):
        errors.append("教师姓名必须是字符串")
    elif teacher and len(teacher) > 10:
        errors.append("教师姓名不能超过10个字符")

    if total_head is not None:
        if not isinstance(total_head, int) or total_head <= 0:
            errors.append("总头数必须是大于0的整数")

    return errors

def validate_password_change(data):
    """验证密码修改数据"""
    errors = []
    old_password = data.get('old_password')
    new_password = data.get('new_password')

    if not old_password:
        errors.append("旧密码不能为空")
    elif not isinstance(old_password, str):
        errors.append("旧密码必须是字符串")
    elif len(old_password) < 6 or len(old_password) > 15:
        errors.append("旧密码长度必须在6-15个字符之间")

    if not new_password:
        errors.append("新密码不能为空")
    elif not isinstance(new_password, str):
        errors.append("新密码必须是字符串")
    elif len(new_password) < 6 or len(new_password) > 15:
        errors.append("新密码长度必须在6-15个字符之间")
    elif old_password == new_password:
        errors.append("新密码不能与旧密码相同")

    return errors 