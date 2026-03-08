create database class3db;

use class3db;

create table students (
student_id int not null	primary key,
name varchar(50),
course varchar(50));

desc students;

Alter table students
add address varchar(100);

desc students;

alter table students
modify name varchar(100);

alter table students
rename column address to std_address;

desc students;

insert into students value
(1, "deep", "data science" , "delhi");


select * from students;

truncate students;



alter table students
add height_cm float;

alter table students
add Enroll boolean;

alter table students
modify student_id int auto_increment; 

-- practice sql 

desc  students;

-- remove primary key 
ALTER TABLE students MODIFY student_id INT;  -- if auto_increment present remove it

alter table students
drop primary key ;

alter table students
add constraint pk_for primary key(name, course);

desc students;

ALTER TABLE students
DROP CONSTRAINT pk_for;

SELECT CONSTRAINT_NAME	
FROM information_schema.TABLE_CONSTRAINTS
WHERE TABLE_NAME = 'students' AND CONSTRAINT_TYPE = 'PRIMARY KEY';

