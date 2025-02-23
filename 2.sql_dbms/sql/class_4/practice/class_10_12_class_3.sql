-- add datatypes and constraints
use class_11_1;

show tables;
drop table student;

-- create table
create table students 
(
 std_id int primary key,
 name varchar(100) not null ,
 phone_number int unique,
 course varchar(100) default "data science",
 age int 
 check (age>=18));

 -- insert value 
 insert into students values
 (2,"rohit",875565656,"ds" ,19), 
 (3, "dev", 095565656, "da",21),
(4, "aniket",65656566, "dwd",22);

-- show data
select* from students;

 insert into students values
 (6,"raaj",87734556,default ,18);
 
 
 -- create course table 
 create table course (
 c_id int primary key,
 course_name varchar(100) not null  unique,
 fee float  not null) ;
 
 describe course;
 
 insert into course values (
 1, "data science", 30000),
 (2, "data analyst", 11000),
 (3, "web development", 15000),
 (4, "full stack", 20000);
 
 select * from course;
 select * from students;
 
 -- add new column in students table 
 alter table students 
 add column course_id varchar(100);
 
 -- delete column
 alter table students
 drop column course_id,
 drop column course;
 
 -- add foregin key
  alter table students 
 add column course_id varchar(100);
 
-- modify column
alter table students
modify column course_id int;

alter table students
add constraint foreign key(course_id) references course(c_id);

desc students;

select * from students;

-- update course_id
update students
set course_id = 1
where std_id =4;

update students
set course_id = 3;
select * from students;
-- 
select name , course_name from students
join course 
on students.course_id =course.c_id;