-- 1. Create the 'stu' database if it doesn't exist
DROP DATABASE IF EXISTS stu;
CREATE DATABASE stu;

-- Use the 'stu' database
USE stu;

-- 2. Create the 'students' table
CREATE TABLE IF NOT EXISTS students (
    student_id INT AUTO_INCREMENT PRIMARY KEY,                 -- Unique identifier for each student
    name VARCHAR(255) NOT NULL,                                 -- Student's full name (not null)
    gender CHAR(1) CHECK(gender IN ('M', 'F')) NOT NULL,        -- Gender of the student (only M or F)
    student_number VARCHAR(20) UNIQUE NOT NULL,                 -- Unique student number
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,             -- Timestamp of record creation
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP  -- Timestamp of last update
);

-- 3. Create the 'course_information' table
CREATE TABLE IF NOT EXISTS course_information (
    course_number VARCHAR(20) PRIMARY KEY,                      -- Unique course number
    course_name VARCHAR(255) NOT NULL,                           -- Name of the course (not null)
    course_opening_semester VARCHAR(50) NOT NULL,                -- Opening semester (not null)
    course_department VARCHAR(100) NOT NULL,                     -- Department offering the course
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,             -- Timestamp of record creation
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP  -- Timestamp of last update
);

-- 4. Create the 'student_grades' table
CREATE TABLE IF NOT EXISTS student_grades (
    student_number VARCHAR(20),                                  -- Foreign key referencing student_number
    course_number VARCHAR(20),                                   -- Foreign key referencing course_number
    grade DECIMAL(5, 2) CHECK(grade >= 0 AND grade <= 100),       -- Student grade (0-100 range)
    grade_number VARCHAR(255),                                   -- Column for storing concatenated student_number and course_number
    UNIQUE (grade_number),                                        -- Ensure the grade_number is unique
    PRIMARY KEY (student_number, course_number),                  -- Composite primary key using student_number and course_number
    FOREIGN KEY (student_number) REFERENCES students(student_number) ON DELETE CASCADE,  -- Referential integrity for students
    FOREIGN KEY (course_number) REFERENCES course_information(course_number) ON DELETE CASCADE,  -- Referential integrity for courses
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,              -- Timestamp of grade record creation
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP  -- Timestamp of last update
);

-- 5. Create the trigger to automatically populate grade_number
DELIMITER //
CREATE TRIGGER before_insert_student_grades
BEFORE INSERT ON student_grades
FOR EACH ROW
BEGIN
    SET NEW.grade_number = CONCAT(NEW.student_number, ':', NEW.course_number);
END;
//
DELIMITER ;

INSERT INTO students (name, gender, student_number)
VALUES 
    ('张三', 'M', 'S10001'),
    ('李四', 'F', 'S10002'),
    ('王五', 'M', 'S10003');

INSERT INTO course_information (course_number, course_name, course_opening_semester, course_department)
VALUES
    ('C101', '数据库原理', '2025-春季', '计算机科学与技术'),
    ('C102', '操作系统', '2025-秋季', '计算机科学与技术'),
    ('C103', '离散数学', '2025-春季', '数学与应用数学');
    
INSERT INTO student_grades (student_number, course_number, grade)
VALUES
    ('S10001', 'C101', 85.50),  -- 张三在数据库原理课程的成绩
    ('S10002', 'C101', 90.00),  -- 李四在数据库原理课程的成绩
    ('S10003', 'C102', 78.00),  -- 王五在操作系统课程的成绩
    ('S10001', 'C103', 88.00);  -- 张三在离散数学课程的成绩

