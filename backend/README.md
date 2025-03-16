# 预排课系统后端

这是预排课系统的后端服务，基于Python Flask框架开发。

## 环境要求

- Python 3.8+
- MySQL 5.7+
- pip（Python包管理器）

## 项目设置

1. 创建并激活虚拟环境：
```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

2. 安装依赖：
```bash
pip install -r requirements.txt
```

3. 配置环境变量：
- 修改`.env`文件中的配置（数据库连接等）

4. 初始化数据库：
- 确保MySQL服务已启动
- 导入SQL文件：
  ```bash
  mysql -u your_username -p your_database < user_info.sql
  mysql -u your_username -p your_database < 教师信息.sql
  mysql -u your_username -p your_database < 本学年课程信息.sql
  mysql -u your_username -p your_database < 历史课表.sql
  ```

## 启动服务

```bash
# 开发模式启动
python app.py

# 或使用 Flask 命令
flask run
```

服务将在 http://localhost:5000 启动

## 项目结构

```
backend/
├── app.py          # 主应用文件，包含所有API路由
├── database.py     # 数据库操作模块
├── auth.py         # 认证相关功能
├── utils.py        # 工具函数
├── validators.py   # 数据验证模块
├── logger.py       # 日志配置
└── requirements.txt # 项目依赖
```

## API文档

### 认证相关
- POST /admin/login - 用户登录
- POST /admin/fixpwd - 修改密码

### 课程管理
- GET /courses - 获取课程列表
- POST /courses - 添加新课程
- PUT /courses - 修改课程信息
- DELETE /courses - 删除课程

### 教师管理
- GET /teacher - 获取教师列表

### 历史课程
- GET /history_courses - 查询历史课程信息 