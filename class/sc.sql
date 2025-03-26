-- create data base
create database class310; 
use class310;

-- create student table 
create table students (
	std_id int primary key,
    name varchar(100) not null,
    course varchar(100) default "data science",
    fee float check( fee>50000),
    enroll_time date 
);
show tables;
describe students;

alter table students
modify column fee int  not null;

-- alter database class310 modify name=class312;
-- RENAME DATABASE class310 TO class312;
CREATE DATABASE class312;

CREATE TABLE class312.students LIKE class310.students;
INSERT INTO class312.students SELECT * FROM class310.students;


-- backup 
-- mysqldump -u root -p class310 > class310_backup.sql