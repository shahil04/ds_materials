create database weekend1012db; -- create database

use weekend1012db;  -- go inside to created weekend database so inside weekned create table

-- create table  with columns define
create table students (
student_id int,
name varchar(50),
address varchar(100),
Phone_number int,
course varchar(30)
);

show tables; -- see how many tables in weekend1012db  
desc students; -- see all columns of students table
select	* from students; -- show the data in students table

-- insert the data into students table
insert into students values 
(11, "raj","delhi",9788,"Data Science"),
(22, "deep", "mumbai", 9999,"web development"),
(33, "sam","Mumbai", 88888,"web development")
;

select	* from students;

-- delete the indisuals row data
delete from students 
where student_id =33;

-- delete the data but not delete the table column names or structure
truncate table students;

-- delete table data as well as the all columns names or structure also 
drop table  students;

-- delete the database 
drop database  weekend1012db;

SET SQL_SAFE_UPDATES = 0;
