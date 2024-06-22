-- 创建数据库
create database if not exists learning;
use learning;






-- 创建学生表
CREATE TABLE IF NOT EXISTS Student (
    StudentID VARCHAR(20) PRIMARY KEY, -- 学号
    StudentName VARCHAR(50), -- 学生姓名
    StudentGender CHAR(1), -- 学生性别
    StudentIDNumber VARCHAR(20), -- 学生身份证号码
    StudentDormitory VARCHAR(50), -- 学生宿舍号
    StudentGrade INT, -- 学生年级
    EarnedCredits INT, -- 已修学分
    RequiredCredits INT, -- 要求修习的学分
    DepartmentID VARCHAR(20), -- 院系ID
    FOREIGN KEY (DepartmentID) REFERENCES Department(DepartmentID) -- 外键关联到院系表
);
-- 插入学生记录
INSERT INTO Student (
    StudentID, StudentName, StudentGender, StudentIDNumber, StudentDormitory, 
    StudentGrade, EarnedCredits, RequiredCredits, DepartmentID) 
VALUES
('220001', '张三', 'M', '123456789012345678', '1栋101', 1, 30, 120, 'D001'),
('220002', '李四', 'F', '234567890123456789', '2栋202', 2, 60, 120, 'D002'),
('220003', '王五', 'M', '345678901234567890', '3栋303', 3, 90, 120, 'D003'),
('220004', '赵六', 'F', '456789012345678901', '4栋404', 4, 120, 120, 'D004'),
('220005', '钱七', 'M', '567890123456789012', '5栋505', 1, 30, 120, 'D001');

select * from Student;






-- 创建课程表
CREATE TABLE IF NOT EXISTS Course (
    CourseID VARCHAR(20) PRIMARY KEY, -- 课程ID
    CourseName VARCHAR(100), -- 课程名称
    TeacherID VARCHAR(20), -- 教师ID
    DepartmentID VARCHAR(20), -- 院系ID
    CourseDescription TEXT, -- 课程描述
    CourseCredits INT, -- 课程学分
    CourseTerm VARCHAR(10), -- 课程学期
    FOREIGN KEY (TeacherID) REFERENCES Teacher(TeacherID), -- 外键关联到教师表
    FOREIGN KEY (DepartmentID) REFERENCES Department(DepartmentID) -- 外键关联到院系表
);

INSERT INTO Course 
(CourseID, CourseName, TeacherID, DepartmentID, CourseDescription, CourseCredits, CourseTerm)
VALUES
    ('C0001', '数据库及实现', 'T0001', 'D001', '介绍数据库基本概念及其在实际应用中的实现方法。', 4, '2024春季'),
    ('C0002', '计算机网络原理', 'T0002', 'D002', '深入理解计算机网络的基本原理及其协议。', 3, '2024秋季'),
    ('C0003', '数据结构与算法', 'T0003', 'D003', '学习数据结构和算法的基本概念及其应用。', 4, '2024秋季');

select * from Course;






-- 创建成绩表
CREATE TABLE IF NOT EXISTS Grade (
    GradeID VARCHAR(20) PRIMARY KEY, -- 成绩ID
    CourseID VARCHAR(20), -- 课程ID
    StudentID VARCHAR(20), -- 学生ID
    GradeLevel CHAR(2), -- 成绩等级
    FOREIGN KEY (CourseID) REFERENCES Course(CourseID), -- 外键关联到课程表
    FOREIGN KEY (StudentID) REFERENCES Student(StudentID) -- 外键关联到学生表
);

INSERT INTO Grade 
(GradeID, CourseID, StudentID, GradeLevel)
VALUES
    ('G0001', 'C0001', '220001', 'A'),
    ('G0002', 'C0002', '220002', 'B+'),
    ('G0003', 'C0003', '220003', 'A-');

select * from Grade;







-- 创建院系表
CREATE TABLE IF NOT EXISTS Department (
    DepartmentID VARCHAR(20) PRIMARY KEY, -- 院系ID
    DepartmentName VARCHAR(100), -- 院系名称
    DepartmentPhone VARCHAR(20), -- 院系电话
    DepartmentOffice VARCHAR(100) -- 院系办公室地址
);

-- 插入院系记录
INSERT INTO Department (
    DepartmentID, DepartmentName, DepartmentPhone, DepartmentOffice
) VALUES
('D001', '大数据学院', '010-12345678', 'A栋101'),
('D002', '计算机学院', '010-87654321', 'B栋202'),
('D003', '信息工程学院', '010-23456789', 'C栋303'),
('D004', '软件学院', '010-34567890', 'D栋404'),
('D005', '电子工程学院', '010-45678901', 'E栋505');

select * from Department;







-- 创建教师表
CREATE TABLE IF NOT EXISTS Teacher (
    TeacherID VARCHAR(20) PRIMARY KEY, -- 教师ID
    TeacherName VARCHAR(50), -- 教师姓名
    TeacherGender CHAR(1), -- 教师性别
    DepartmentID VARCHAR(20), -- 院系ID
    TeacherPhone VARCHAR(20), -- 教师电话
    TeacherOffice VARCHAR(100), -- 教师办公室
    FOREIGN KEY (DepartmentID) REFERENCES Department(DepartmentID) -- 外键关联到院系表
);

-- 插入教师记录
INSERT INTO Teacher (
    TeacherID, TeacherName, TeacherGender, DepartmentID, TeacherPhone, TeacherOffice
) VALUES
('T0001', '张大数据', 'M', 'D001', '010-12345678', 'A栋201'),
('T0002', '李计算', 'F', 'D002', '010-87654321', 'B栋202'),
('T0003', '王信息', 'M', 'D003', '010-23456789', 'C栋303'),
('T0004', '赵软件', 'F', 'D004', '010-34567890', 'D栋404'),
('T0005', '钱电子', 'M', 'D005', '010-45678901', 'E栋505');

select * from Teacher;








-- 创建院系主任表
CREATE TABLE IF NOT EXISTS DepartmentHead (
    HeadID VARCHAR(20) PRIMARY KEY, -- 院系主任ID
    HeadName VARCHAR(50), -- 院系主任姓名
    HeadGender CHAR(1), -- 院系主任性别
    DepartmentID VARCHAR(20), -- 院系ID
    HeadPhone VARCHAR(20), -- 院系主任电话
    HeadOffice VARCHAR(100), -- 院系主任办公室
    HeadEmail VARCHAR(100), --院系主任邮箱
    FOREIGN KEY (DepartmentID) REFERENCES Department(DepartmentID) -- 外键关联到院系表
);

-- 插入院系主任记录
INSERT INTO DepartmentHead (
    HeadID, HeadName, HeadGender, DepartmentID, HeadPhone, HeadOffice
) VALUES
('DH0001', '王大数据', 'M', 'D001', '010-12345678', 'A栋301'),
('DH0002', '李计算', 'F', 'D002', '010-87654321', 'B栋302'),
('DH0003', '张信息', 'M', 'D003', '010-23456789', 'C栋303'),
('DH0004', '赵软件', 'F', 'D004', '010-34567890', 'D栋304'),
('DH0005', '钱电子', 'M', 'D005', '010-45678901', 'E栋305');


select * from DepartmentHead;







-- 创建院系管理员表
CREATE TABLE IF NOT EXISTS DepartmentAdmin (
    AdminID VARCHAR(20) PRIMARY KEY, -- 管理员ID
    AdminName VARCHAR(50), -- 管理员姓名
    AdminGender CHAR(1), -- 管理员性别
    AdminPhone VARCHAR(20), -- 管理员电话
    AdminOffice VARCHAR(100) -- 管理员办公室
);

-- 插入院系管理员记录
INSERT INTO DepartmentAdmin (
    AdminID, AdminName, AdminGender, AdminPhone, AdminOffice
) VALUES
('A0001', '刘管理员', 'M', '010-12345678', 'A栋401'),
('A0002', '陈管理员', 'F', '010-87654321', 'B栋402'),
('A0003', '杨管理员', 'M', '010-23456789', 'C栋403'),
('A0004', '吴管理员', 'F', '010-34567890', 'D栋404'),
('A0005', '赵管理员', 'M', '010-45678901', 'E栋405');


select * from DepartmentAdmin;






-- 创建选修表
CREATE TABLE IF NOT EXISTS Enrollment (
    StudentID VARCHAR(20), -- 学生ID
    CourseID VARCHAR(20), -- 课程ID
    PRIMARY KEY (StudentID, CourseID), -- 复合主键
    FOREIGN KEY (StudentID) REFERENCES Student(StudentID), -- 外键关联到学生表
    FOREIGN KEY (CourseID) REFERENCES Course(CourseID) -- 外键关联到课程表
);


-- 插入值到 Enrollment 表
INSERT INTO Enrollment (StudentID, CourseID) VALUES ('220001', 'C0001'),
('220002', 'C0002'),
('220003', 'C0003');


select * from Enrollment;




-- 创建归属表
CREATE TABLE IF NOT EXISTS BelongTo (
    StudentID VARCHAR(20), -- 学生ID
    DepartmentID VARCHAR(20), -- 院系ID
    PRIMARY KEY (StudentID, DepartmentID), -- 复合主键
    FOREIGN KEY (StudentID) REFERENCES Student(StudentID), -- 外键关联到学生表
    FOREIGN KEY (DepartmentID) REFERENCES Department(DepartmentID) -- 外键关联到院系表
);

-- 插入值到 BelongTo 表
INSERT INTO BelongTo (StudentID, DepartmentID) VALUES ('220001', 'D001'),
('220002', 'D002'),
('220003', 'D003'),
('220004', 'D004');

select * from BelongTo









-- 创建开设表
CREATE TABLE IF NOT EXISTS Offer (
    CourseID VARCHAR(20), -- 课程ID
    DepartmentID VARCHAR(20), -- 院系ID
    PRIMARY KEY (CourseID, DepartmentID), -- 复合主键
    FOREIGN KEY (CourseID) REFERENCES Course(CourseID), -- 外键关联到课程表
    FOREIGN KEY (DepartmentID) REFERENCES Department(DepartmentID) -- 外键关联到院系表
);

-- 插入值到 Offer 表
INSERT INTO Offer (CourseID, DepartmentID) VALUES 
('C0001', 'D001'),
('C0002', 'D002'),
('C0003', 'D003');

select * from Offer;








-- 创建录入表
CREATE TABLE IF NOT EXISTS Record (
    TeacherID VARCHAR(20), -- 教师ID
    GradeID VARCHAR(20), -- 成绩ID
    RecordTime TIMESTAMP, -- 录入时间
    PRIMARY KEY (TeacherID, GradeID), -- 复合主键
    FOREIGN KEY (TeacherID) REFERENCES Teacher(TeacherID), -- 外键关联到教师表
    FOREIGN KEY (GradeID) REFERENCES Grade(GradeID) -- 外键关联到成绩表
);

-- 插入值到 Record 表
INSERT INTO Record (TeacherID, GradeID, RecordTime) VALUES 
('T0001', 'G0001', CURRENT_TIMESTAMP),
('T0002', 'G0002', CURRENT_TIMESTAMP),
('T0003', 'G0003', CURRENT_TIMESTAMP);


select * from Record;







-- 创建院系管理表
CREATE TABLE IF NOT EXISTS Manage (
    AdminID VARCHAR(20), -- 管理员ID
    DepartmentID VARCHAR(20), -- 院系ID
    ManageStartDate DATE, -- 管理开始日期
    PRIMARY KEY (AdminID, DepartmentID), -- 复合主键
    FOREIGN KEY (AdminID) REFERENCES DepartmentAdmin(AdminID), -- 外键关联到院系管理员表
    FOREIGN KEY (DepartmentID) REFERENCES Department(DepartmentID) -- 外键关联到院系表
);

-- 插入值到 Manage 表
INSERT INTO Manage (AdminID, DepartmentID, ManageStartDate) VALUES ('A0001', 'D001', '2024-01-01'),
 ('A0002', 'D002', '2024-02-01'),
 ('A0003', 'D003', '2024-03-01'),
 ('A0004', 'D004', '2024-04-01'),
('A0005', 'D005', '2024-05-01');

select * from Manage;








-- 创建教师管理表
CREATE TABLE IF NOT EXISTS TeacherManage (
    HeadID VARCHAR(20), -- 院系主任ID
    TeacherID VARCHAR(20), -- 教师ID
    ManageStartDate DATE, -- 管理开始日期
    PRIMARY KEY (HeadID, TeacherID), -- 复合主键
    FOREIGN KEY (HeadID) REFERENCES DepartmentHead(HeadID), -- 外键关联到院系主任表
    FOREIGN KEY (TeacherID) REFERENCES Teacher(TeacherID) -- 外键关联到教师表
);

-- 插入值到 TeacherManage 表
INSERT INTO TeacherManage (HeadID, TeacherID, ManageStartDate) VALUES ('DH0001', 'T0001', '2024-01-01'),
('DH0002', 'T0002', '2024-02-01'),
 ('DH0003', 'T0003', '2024-03-01'),
('DH0004', 'T0004', '2024-04-01'),
('DH0005', 'T0005', '2024-05-01');


select * from TeacherManage;










-- 创建密码表
CREATE TABLE IF NOT EXISTS Passwords (
    ID VARCHAR(20) PRIMARY KEY, -- 学生学号或工号
    Role ENUM('Student', 'Teacher', 'DepartmentHead', 'Admin'), -- 角色
    Password VARCHAR(255) -- 密码（假设存储为加密后的密码）
);


-- 插入记录时，必须选择预定义的角色之一
INSERT INTO Passwords (ID, Role, Password) VALUES 
('220001', 'Student', '123456'),
('T0001', 'Teacher', '123456'),
('DH0001', 'DepartmentHead', '123456'),
('A0001', 'Admin', '123456');

select * from Passwords;






