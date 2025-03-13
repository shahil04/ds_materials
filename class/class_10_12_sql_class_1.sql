-- show the database 
show databases; 
-- access the database using use keywords
use mavenmovies;

-- show the all table in a single database 
show tables;

-- show the structure of a single table 
desc actor;

-- show the all data from actor table
select * from actor;

-- DDL
-- Create 
-- database , table

-- create data base
create database class310; 
use class310;

-- create student table 
create table students (
	std_id int,
    name varchar(100),
    course varchar(100),
    fee float,
    enroll_time date
);
show tables;
desc students;
describe students;

-- show all data
select * from students;

-- insert data into table
-- syntax
-- INSERT INTO table_name (column1, column2, column3, ...)
-- VALUES (value1, value2, value3, ...);

insert into students (std_id, name , course,fee, enroll_time)
value (1, "raj","ds",20000,'2025-02-12');

insert into students
value (2, "jeet","ds",322000,'2025-02-22');

-- store multiple values
insert into students
value (4, "jeeet","ds",3000,'2025-02-22'),
	(3,"alok", "da",10000,"2024-02-25")
;

-- alter  for columns updates
-- add new columns 
alter table students
add discount float, add xyz int; 

-- delete the columns
alter table students
drop column xyz;

desc students;
-- change datatypes and constraints
alter table students
modify column discount int;

-- rename the column name 
alter table students 
rename column enroll_time  to enroll_date;

truncate table students;
select * from students;

drop table students;
drop database class310;