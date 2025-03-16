"""
预排课系统日志配置模块
功能：
1. 配置日志格式和级别
2. 提供文件和控制台日志输出
3. 定义不同级别的日志处理器
"""

import logging
import os
from logging.handlers import RotatingFileHandler

# 创建logs目录（如果不存在）
if not os.path.exists('logs'):
    os.makedirs('logs')

# 创建日志记录器
logger = logging.getLogger('pre_schedule_sys')
logger.setLevel(logging.INFO)

# 日志格式
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# 文件处理器（按大小轮转）
file_handler = RotatingFileHandler(
    'logs/app.log',
    maxBytes=10*1024*1024,  # 10MB
    backupCount=5,
    encoding='utf-8'
)
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(formatter)

# 控制台处理器
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(formatter)

# 添加处理器到日志记录器
logger.addHandler(file_handler)
logger.addHandler(console_handler)

def get_logger():
    return logger 