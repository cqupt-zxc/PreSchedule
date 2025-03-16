# 预排课系统数据库文件

本目录包含预排课系统所需的所有数据库文件和配置信息。

## 数据库结构

### 1. user_info（用户信息表）
- 存储系统用户信息
- 包含账号、密码、角色等字段

### 2. 教师信息表
- 存储教师基本信息
- 包含姓名、序号、备注等字段

### 3. 本学年课程信息表
- 存储当前学年的课程安排
- 包含课程名称、教师、学时、学生人数等信息

### 4. 历史课表
- 存储历史学期的课程记录
- 用于课程统计和历史数据查询

## 数据库初始化步骤

1. 确保MySQL服务已启动

2. 创建数据库：
```sql
CREATE DATABASE IF NOT EXISTS pre_schedule_sys CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

3. 使用数据库：
```sql
USE pre_schedule_sys;
```

4. 导入表结构和数据：
```bash
# Windows 环境下
mysql -u root -p pre_schedule_sys < user_info.sql
mysql -u root -p pre_schedule_sys < 教师信息.sql
mysql -u root -p pre_schedule_sys < 本学年课程信息.sql
mysql -u root -p pre_schedule_sys < 历史课表.sql

# Linux/Mac 环境下
mysql -u root -p pre_schedule_sys < user_info.sql
mysql -u root -p pre_schedule_sys < 教师信息.sql
mysql -u root -p pre_schedule_sys < 本学年课程信息.sql
mysql -u root -p pre_schedule_sys < 历史课表.sql
```

## 数据库备份

建议定期备份数据库：
```bash
# 备份
mysqldump -u root -p pre_schedule_sys > backup_$(date +%Y%m%d).sql

# 恢复
mysql -u root -p pre_schedule_sys < backup_filename.sql
```

注意：数据库连接配置请参考backend目录下的README.md文件。 