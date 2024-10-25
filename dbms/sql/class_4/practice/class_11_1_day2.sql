-- show all the db
show databases;

-- create database
-- create database dbname
create database class_11_1;

-- database activate 
use class_11_1;

-- check table are there or not 
show tables;

-- create table  
--  create table tablename (col_name datatypes constraints)
create table student ( id int , name varchar(100), course varchar(100), fee float );

show tables;

-- show structure of table of student (cols name , datypes, constrainst
desc student;

-- show temporaty view of data in table format
select *  from student;

-- insert data into student table 
insert into student value (1, "aznaan","data science", 10000);

insert into student values (2,"rohit","ds" ,10000), (3, "dev", "da",11000),
							(4, "aniket","dwd",11000);
-- show data 
select * from student;

-- only show select columns data
select name ,fee  from student;

-- if you want update the data of indivisual row based on condition
update student 
set course ="data science"
where name ="dev";


-- update multiple values
update student 
set course ="data science", fee=20000
where name ="dev";


-- delete indivisula data 
delete from student 
where name = "aznaan";

select * from student;

-- truncate delete all data excpet the table structure
truncate table student;

-- -- drop  - delete table as well as delete data
drop table student;

-- delete the database
drop database class_11_1;


