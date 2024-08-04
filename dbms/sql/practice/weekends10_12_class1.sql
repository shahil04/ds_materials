create database weekend1012db; -- create database

use weekend1012db;  -- implement the created database
#  /*
-- create table 
create table students (
student_id int,
name varchar(50),
address varchar(100),
Phone_number int,
course varchar(30)
);
 show tables;
desc students;
select	* from students;

insert into students values 
(11, "raj","delhi",9788,"Data Science"),
(22, "deep", "mumbai", 9999,"web development"),
(33, "sam","Mumbai", 88888,"web development")
;

select	* from students;

delete from students 
where student_id =33;
-- 
truncate table students;

drop table  students;

drop database  weekend1012db;

SET SQL_SAFE_UPDATES = 0;
