"""
预排课系统工具函数模块
功能：
1. 提供教师姓名的格式化和清理
2. 解析教师姓名和课程头数
3. 处理教师列表的分割和转换
4. 提供通用的字符串处理工具

"""

import re
def format_teacher_name(name, headcount):
    """格式化教师姓名和头数"""
    return f"{name} ({headcount})"


def clean_teacher_name(teacher_name):
    """清理教师姓名，去除多余的空格和换行符"""
    return teacher_name.strip().replace('\n', '').replace('\r', '')
def parse_teacher_name_and_headcount(teacher_str):
    """解析教师姓名和头数，默认头数为1"""
    teacher_str = str(teacher_str).strip()

    # 使用正则表达式匹配带括号的头数信息
    match = re.search(r'[(（]\s*(\d+)\s*[)）]', teacher_str)

    if match:
        headcount = int(match.group(1))
        full_teacher_name = teacher_str.strip()  # 完整的教师姓名（包括括号内的头数）
        teacher_name_without_headcount = re.sub(r'[(（]\s*\d+\s*[)）]', '', teacher_str).strip()  # 去掉括号及其内部的内容
    else:
        full_teacher_name = teacher_str.strip()
        teacher_name_without_headcount = teacher_str.strip()
        headcount = 1  # 默认头数

    return full_teacher_name, teacher_name_without_headcount, headcount


def split_teachers(teachers_array):
    """将教师姓名数组转换为列表"""
    return [str(teacher).strip() for teacher in teachers_array if str(teacher).strip()]










