# 预排课系统

这是一个基于Vue 3 + Flask的预排课系统，用于管理和安排课程信息。

## 项目结构

```
COUPT-PSS/

├── frontend/          # 前端项目目录
│   ├── src/          # 源代码
│   ├── public/       # 静态资源
│   └── package.json  # 项目依赖配置
│
├── backend/          # 后端项目目录
│   ├── app.py       # 主应用文件
│   ├── database.py  # 数据库操作
│   ├── auth.py      # 认证相关
│   ├── utils.py     # 工具函数
│   └── validators.py # 数据验证
│
├── database/        # 数据库文件目录
│   ├── user_info.sql        # 用户信息表
│   ├── 教师信息.sql         # 教师基本信息
│   ├── 本学年课程信息.sql   # 当前课程数据
│   └── 历史课表.sql        # 历史课程记录
│
└── .idea/           # JetBrains IDE配置文件夹（可删除）
```

## 环境要求

### 前端
- Node.js 14+
- npm 6+

### 后端
- Python 3.8+
- MySQL 5.7+
- pip（Python包管理器）

## 快速开始

### 1. 数据库设置

1. 确保MySQL服务已启动

2. 创建数据库：
```sql
CREATE DATABASE IF NOT EXISTS pre_schedule_sys CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

3. 导入数据（数据需根据自己课程和教师情况自行导入）：
```bash
cd database
mysql -u root -p pre_schedule_sys < user_info.sql
mysql -u root -p pre_schedule_sys < 教师信息.sql
mysql -u root -p pre_schedule_sys < 本学年课程信息.sql
mysql -u root -p pre_schedule_sys < 历史课表.sql

-- 插入用户信息示例
INSERT INTO pre_schedule_sys.user_info (id, account, password, role) VALUES (1, 'your_account', '$2b$12$your_password_hash', 'your_role');

-- 插入教师信息示例
INSERT INTO pre_schedule_sys.教师信息 (序号, 姓名, 职工号, 办公电话, 移动电话, 电子邮箱, 备注) VALUES (1, 'your_teacher_name', 'your_employee_number', 'your_office_phone', 'your_mobile_phone', 'your_email', 'your_note');

-- 插入本学年课程信息示例
INSERT INTO pre_schedule_sys.本学年课程信息 (学年学期, 课程名称, 教师姓名, 学时, 头数, 学生人数, 总头数) VALUES ('your_semester', 'your_course_name', 'your_teacher_name', your_class_hours, your_headcount, your_student_number, your_total_headcount);

-- 插入历史课表信息示例
INSERT INTO `历史课表` (`学年学期`, `课程名称`, `任课教师`) VALUES ('your_semester', 'your_course_name', 'your_teacher_name');
```


### 2. 后端设置

1. 进入后端目录：
```bash
cd backend
```

2. 创建并激活虚拟环境：
```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

3. 安装依赖：
```bash
pip install -r requirements.txt
```

4. 配置环境变量：
- 复制`.env.example`为`.env`
- 修改数据库连接信息：
```
DB_USER=your_username
DB_PASSWORD=your_password
DB_HOST=localhost
DB_DATABASE=pre_schedule_sys
SECRET_KEY=your_secret_key
```

5. 启动后端服务：
```bash
python app.py
```
服务将在 http://localhost:5000 启动

### 3. 前端设置

1. 进入前端目录：
```bash
cd frontend
```

2. 安装依赖：
```bash
npm install
```

3. 启动开发服务器：
```bash
npm run dev
```
前端将在 http://localhost:5173 启动

## 主要功能

### 用户管理
- 用户登录
- 密码修改
- 权限控制

### 课程管理
- 课程信息录入
- 课程信息修改
- 课程信息删除
- 课程信息查询

### 教师管理
- 教师信息查询
- 教师课程分配

### 历史数据
- 历史课程查询
- 学期数据统计

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

## 开发说明

### 前端
- 使用Vue 3 + TypeScript开发
- 使用Element Plus组件库
- 采用Vite作为构建工具
- 支持热重载开发

### 后端
- 使用Flask框架开发
- 采用MySQL数据库
- JWT认证
- 统一的错误处理
- 完整的日志记录

## 注意事项

1. 确保MySQL服务正常运行
2. 检查数据库连接配置
3. 前端API地址配置正确
4. 保持.env文件的安全性
5. 定期备份数据库
6. .idea文件夹是JetBrains IDE（如WebStorm、PyCharm）的项目配置文件夹，可以安全删除，不影响项目运行

## 常见问题

1. 数据库连接失败
   - 检查MySQL服务是否启动
   - 验证数据库用户名和密码
   - 确认数据库名称正确

2. 前端API调用失败
   - 检查后端服务是否启动
   - 验证API地址配置
   - 确认跨域设置正确

3. 登录失败
   - 验证用户名和密码
   - 检查数据库中的用户信息
   - 确认JWT配置正确 
