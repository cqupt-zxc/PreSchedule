"""
预排课系统认证模块
功能：
1. 实现JWT token的生成和验证
2. 处理用户身份验证
3. 提供用户权限检查
4. 管理token的过期和刷新

依赖：
- PyJWT
- python-dotenv
- Flask
"""

from datetime import datetime, timedelta
import jwt
from flask import request
from flask import current_app
from dotenv import load_dotenv
import os

# 加载.env文件中的环境变量
load_dotenv()

# 从环境变量中获取SECRET_KEY
SECRET_KEY = os.getenv('SECRET_KEY')


def generate_token(account, user_id, role, expires_days=7):
    """生成 token 的辅助函数"""
    payload = {
        "account": account,
        "id": user_id,
        "role": role,
        "exp": datetime.utcnow() + timedelta(days=expires_days)
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return token


def get_current_user_from_token():
    """从请求头中获取当前用户信息"""
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return None
    token = auth_header.split(' ')[1]  # 提取 token
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        return None  # Token 已过期
    except jwt.InvalidTokenError:
        return None  # Token 无效


def verify_token(token, secret_key):
    try:
        payload = jwt.decode(token, secret_key, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None
def is_admin(current_user):
    return current_user and current_user.get('role') == 'admin'