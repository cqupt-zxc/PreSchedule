-- 插入用户信息示例
INSERT INTO pre_schedule_sys.user_info (id, account, password, role) VALUES (1, 'your_account', '$2b$12$your_password_hash', 'your_role');

-- 插入教师信息示例
INSERT INTO pre_schedule_sys.教师信息 (序号, 姓名, 职工号, 办公电话, 移动电话, 电子邮箱, 备注) VALUES (1, 'your_teacher_name', 'your_employee_number', 'your_office_phone', 'your_mobile_phone', 'your_email', 'your_note');

-- 插入本学年课程信息示例
INSERT INTO pre_schedule_sys.本学年课程信息 (学年学期, 课程名称, 教师姓名, 学时, 头数, 学生人数, 总头数) VALUES ('your_semester', 'your_course_name', 'your_teacher_name', your_class_hours, your_headcount, your_student_number, your_total_headcount);

-- 插入历史课表信息示例
INSERT INTO `历史课表` (`学年学期`, `课程名称`, `任课教师`) VALUES ('your_semester', 'your_course_name', 'your_teacher_name');
