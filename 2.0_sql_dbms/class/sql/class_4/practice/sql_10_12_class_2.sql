create database itvedant;

use itvedant;

create table students(
name varchar(100),
id int primary key,
course varchar(100) ,
enrolled binary not null
);
desc students;
alter table students	
modify course varchar(100) default "data science";

-- add new column phone number using alter in students table in itvedant database
alter table students
add phone_nu int;

insert into students values 
("raj", 1, "ds", 1 , 987978899),
("abc",2 ,"web dev",0,545644545),
("deep",3,"cloud",1,985656565);
insert into students values 
("rajj", 5,default, 1 , 987978899);

select name, id , course cs ,convert(enrolled using utf8) as enroll, phone_number from students;
select * from students;

-- rename column 
alter table students
rename column phone_number  to ph_num;
update students 
set name ="veer", course= "MySql"
where id=4;


delete from students 
where id =5;

alter table students
drop phone_nu;

-- example of adding foreign key of student table--> id into address tables --> student_id columns
CREATE TABLE address (
    address_id INT PRIMARY KEY,
    student_id INT,
    street VARCHAR(255),
    city VARCHAR(100),
    state VARCHAR(100),
    postal_code VARCHAR(20),
    FOREIGN KEY (student_id) REFERENCES students(id)
);

alter table students
add course_fee int ;

alter table students
add pay_amount int ;

update students 
set course_fee=10000, pay_amount=2000
where id=4;

select name, course_fee - pay_amount as due from students;

select name, id , course_fee - pay_amount as due from students
where id <> 2;

-- and 
select name, id , course_fee - pay_amount as due from students
where name="raj" and id= 2;

select name, id , course_fee - pay_amount as due from students
where name="raj" or id= 2;

select name, id , course_fee - pay_amount as due from students
where id<>2;

select * from students;

select * from students
where course_fee is not null;



-- ------------
-- 17-08-24 

create table course (
course_id int , 
course_name varchar(100) not null,
fee int default 85000 ,
primary key (course_id)
);

drop table course;
describe  course;


insert into course  values
(1, "data science" , 90000),
(2, "Web development", 87000),
(3, "full stack", default);

select * from course
where course_id in (1,3);

-- between 
select * from course
where course_id between 1 and 3;

select sum(fee) from course;

select min(fee) from course;

select sum(fee), min(fee), max(fee), avg(fee), count(course_id) total_no_of_course from course;

-- limit
select * from course  limit 2;

select * from course  order by fee desc;  -- asc ,desc 
select * from course  order by fee asc;

select * from course  order by fee desc limit 2;

select * from students;

-- like
select * from students
where name like "%j";

select * from students
where name like "_ee%";



show tables;
select * from actor
where first_name like "a%";

-- use 
use mavenmovies;
select * from payment;

-- in bewteen , where , limit , like , operators
-- aggrigate funtions
-- 
select * from payment
where amount> 5;

-- customer id 10 15, 20 
select * from payment
where customer_id in (10,15, 20);

-- find the details of customerid 10 to 30
select * from payment
where customer_id between 10 and 30;

select distinct(customer_id) from payment
where customer_id between 10 and 30;

select customer_id, sum(amount), avg(amount), min(amount), max(amount), count(amount) from payment
where customer_id between 10 and 30
group by customer_id ;

-- top 5 sales
select * from payment
order by amount desc limit 5;

-- top 5 sales by customers
select customer_id, sum(amount) from payment
group by customer_id
order by  sum(amount) desc 
limit 5;
-- bottom 5 sales 
-- Name of the actor who win the awards name start with  t ( table actor_award)
select * from actor_award;
where awards like "t%";
-- total sales amt, min , max, avg sales
-- no of customer from customer table 
select count(customer_id) as total_customers  from customer;
-- 
select concat(first_name ," - " , last_name) as fn, length(concat(first_name ," - " , last_name)) as no_of_letters from actor_award;


SELECT
    DATE_ADD(NOW(), INTERVAL 1 HOUR) AS added_one_hour,
    DATE_SUB(NOW(), INTERVAL 1 DAY) AS subtracted_one_day,
    EXTRACT(YEAR FROM NOW()) AS extracted_year,
    EXTRACT(MONTH FROM NOW()) AS extracted_month,
    EXTRACT(DAY FROM NOW()) AS extracted_day,
    EXTRACT(HOUR FROM NOW()) AS extracted_hour,
    EXTRACT(MINUTE FROM NOW()) AS extracted_minute,
    EXTRACT(SECOND FROM NOW()) AS extracted_second,
    DATEDIFF('2024-05-30', '2024-05-21') AS date_difference;

select last_update , month(last_update) from actor_award;
select last_update , extract (month from last_update) from actor_award;


select customer_id, sum(amount) from payment
group by customer_id
having sum(amount)>200
order by  sum(amount) desc ;