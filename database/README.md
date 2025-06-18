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

4. 导入表结构：
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
5. 导入自定义数据，需要根据自己的实际情况向数据库中插入数据。可以将下面各表的插入语句示例，根据实际信息进行替换，然后保存为一个名为 your_custom_data.sql 的文件，最后使用该文件导入自定义数据。
```sql
# user_info 表
-- 插入用户信息示例
INSERT INTO pre_schedule_sys.user_info (id, account, password, role) VALUES (1, 'your_account', '$2b$12$your_password_hash', 'your_role');

id：用户的唯一标识，为整数类型。
account：用户的账号，可根据实际情况修改。
password：经过哈希处理后的密码，你需要自行生成。
role：用户的角色，例如 user 或其他自定义角色。
```

```sql
# 教师信息表
-- 插入教师信息示例
INSERT INTO pre_schedule_sys.教师信息 (序号, 姓名, 职工号, 办公电话, 移动电话, 电子邮箱, 备注) VALUES (1, 'your_teacher_name', 'your_employee_number', 'your_office_phone', 'your_mobile_phone', 'your_email', 'your_note');

序号：教师的编号，为整数类型。
姓名：教师的姓名，可根据实际情况修改。
职工号：教师的职工编号，可根据实际情况修改。
办公电话：教师的办公电话号码，可根据实际情况修改。
移动电话：教师的移动电话号码，可根据实际情况修改。
电子邮箱：教师的电子邮箱地址，可根据实际情况修改。
备注：关于教师的备注信息，可根据实际情况修改。
```

```sql
# 本学年课程信息表
-- 插入本学年课程信息示例
INSERT INTO pre_schedule_sys.本学年课程信息 (学年学期, 课程名称, 教师姓名, 学时, 头数, 学生人数, 总头数) VALUES ('your_semester', 'your_course_name', 'your_teacher_name', your_class_hours, your_headcount, your_student_number, your_total_headcount);

学年学期：课程所在的学年和学期，格式如 20242。
课程名称：课程的具体名称，可根据实际情况修改。
教师姓名：授课教师的姓名，可根据实际情况修改。
学时：课程的总学时数，为整数类型。
头数：课程的开课数量，为整数类型。
学生人数：选修该课程的学生数量，为整数类型。
总头数：课程的总开课数量，为整数类型。
```


```sql
#历史课表
-- 插入历史课表信息示例
INSERT INTO `历史课表` (`学年学期`, `课程名称`, `任课教师`) VALUES ('your_semester', 'your_course_name', 'your_teacher_name');

学年学期：课程所在的学年和学期，格式如 20191。
课程名称：课程的具体名称，可根据实际情况修改。
任课教师：授课教师的姓名，可根据实际情况修改。
```
在替换上述示例中的信息后，将这些 SQL 语句保存为 your_custom_data.sql 文件，然后使用以下命令导入到数据库中：
```bash
mysql -u root -p pre_schedule_sys < your_custom_data.sql
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
