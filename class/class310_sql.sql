use mavenmovies;
-- limit 
-- define no. of rows to show 
select * from payment limit 10;
-- 2. order by 

select * from payment 
order by  amount  desc;

-- top 5 payment
select * from payment 
order by  amount  desc
limit 5;

-- coditions
select * from payment 
where  amount>=10
order by  amount  desc
limit 5;

-- show the details of customer id 2
select * from payment
where customer_id =2;

--   use for  multiple values in conditions using or 
select * from payment
where customer_id =2 or customer_id =10 or customer_id =50;

-- IN operators  --> use for  multiple values in conditions
select * from payment
where customer_id  in ( 2,10,50);

-- IN operators  --> use for  multiple values not in  conditions
select * from payment
where customer_id  not in ( 2,10,50);

select * from payment
where customer_id  in ( 2,3,4,5,6,7,8,9,10);

-- Between  operators  --> use for  multiple values  in conditions  if value in range
select * from payment
where customer_id  between 2 and 10;

-- like operators
select * from actor;

-- Q. show the actor  first name is ED
select * from actor
where  first_name="ED";

-- Q. show the actor  first name  start from letter pen*
select * from actor
where  first_name like 'pen%';
-- % for 0 or more than 0 char

-- _ for 1 char 
select * from actor
where  first_name like 'e_';

select * from actor
where  last_name like 's_____';

select * from actor
where  last_name like '%eep';

select * from actor
where  last_name like '%ee%';

select * from actor
where  last_name like '%ee_';

select * from actor
where  last_name like 'mc%n';
-- =====

-- Null or not null 
select * from actor
where  first_name  is null;

select * from actor
where  first_name  is not null;

-- use multiple conditions  on multipe columns
-- find data where fname nick  and last name is stallone 
select * from actor
where  first_name="nick"  and last_name="stallone";

-- use multiple conditions  on multipe columns
-- find data where fname nick  and last name is stallone  or id 4;
select * from actor
where  (first_name="nick"  and last_name="stallone") or actor_id =4;

-- Aggrigate functions
-- sum avg min max ,count
-- total payment
select  sum(amount) from payment;

-- -- total payment top 
select  sum(amount) from payment
where  customer_id between 1 and 10 ;

select  sum(amount) from payment
where  customer_id= 5;

-- Alias for using temperay or nickname of colums
-- using  as keywords or also without as we define
select  sum(amount) as total , 
	max(amount) as maximun_value , 	
    min(amount) minimum_value,
    count(amount) no_of_payment, 
    avg(amount) average_payment
				from payment;

-- show  10 movies from film
-- total inventry 

 -- 19/04/2025
 -- PK ,FK
 
 -- create 
 use class310;
-- create student table 
create table students (
	std_id int  primary key ,
    name varchar(100),
    course varchar(100),
    fee float,
    enroll_time date
    
    -- primary key(std_id)
);
show tables;
desc students;
describe students;

create table course (
	c_id int  ,
    cname varchar(100),
    fee float
    
    -- primary key(std_id)
);

desc course;
-- using alter to add PK
alter table course
add primary key(c_id);

-- refer the course to student table 
-- Forigen key 

alter table students
drop course;

alter table students
add courseid int ,
add   foreign key(courseid) references course(c_id);
describe students;

-- functions
-- 1. aggrigate functions
-- string
-- text , concat, len , left, right , trim , mid

-- 
select "A";

SELECT  WEEK("2017-10-25", 1);
-- String functions;
-- concat
select concat("my" ," ", "sql")  cocat;
use mavenmovies;

select  actor_id,  concat(first_name, ' - ',last_name) full_name from actor;

select   concat(first_name, ' - ',last_name)   full_name, lower(first_name) , 
				trim( first_name) , length(first_name)  ,char_length(first_name)   from actor;
                

select 'hello World', replace('hello World', 'World', 'universe');

select  actor_id,  first_name , replace(first_name, "CK","MK" ) from  actor;

select "   abc" , length ("   abc" ), trim("   abc" )  , length(trim("   abc" ));
select trim(first_name) from actor;

-- Maths 
-- ABS(-10) AS absolute_value,
--    CEIL(4.5) AS ceil_value,
--    FLOOR(4.5) AS floor_value,
--    MOD(10, 3) AS modulus,
--    ROUND(4.567, 2) AS rounded_value
--    EXP(1) AS exponential_value,
--    POW(2, 3) AS power_value,
--    SQRT(25) AS square_root_value;

select 
			abs(-10),
            floor(5.8),
            ceil(5.8),
            mod(10,3),
            10/3,
            round(10/3, 2),
            exp(2),
            power(3,3),
            sqrt(9)
;
select  amount , round (amount, 1) round_off  from payment;


-- Date and time
-- SELECT
--     DATE_ADD(NOW(), INTERVAL 1 HOUR) AS added_one_hour,
--     DATE_SUB(NOW(), INTERVAL 1 DAY) AS subtracted_one_day,
--     EXTRACT(YEAR FROM NOW()) AS extracted_year,
--     EXTRACT(MONTH FROM NOW()) AS extracted_month,
--     EXTRACT(DAY FROM NOW()) AS extracted_day,
--     EXTRACT(HOUR FROM NOW()) AS extracted_hour,
--     EXTRACT(MINUTE FROM NOW()) AS extracted_minute,
--     EXTRACT(SECOND FROM NOW()) AS extracted_second,
--     DATEDIFF('2024-05-30', '2024-05-21') AS date_difference;
-- WEEK("2017-06-15");
-- WEEKDAY
-- SELECT TIME_FORMAT("19:30:10", "%H %i %s");
-- SELECT DATE_FORMAT("2017-06-15", "%Y");
-- ADDDATE(date, INTERVAL value addunit)
-- SELECT ADDDATE("2017-06-15", INTERVAL 10 DAY);-- 

select 
		now(),
        curdate(),
        day( curdate()),
        day('2024-12-21'),
        date("2023,12,23"),
        month('2024-12-21'),
        monthname('2024-12-21'),
        year('2024-12-21')
        ;
        
	select 
		date_add('2024-12-21', interval  5 day),
        date_add('2024-12-21', interval  5 month),
        date_sub('2024-12-21', interval  5 day),
        datediff('2024-12-25', '2024-11-20') , 
        datediff('2024-12-25', '2024-11-20')  div 30  as month ,  -- take intger value 
        mod(datediff('2024-12-25', '2024-11-20'),30 ) as day  
        ;

select 
	extract( month  from "2024-10-21"),
    extract(hour from "2024-10-21 12:23:10") ;
    
select  monthname(payment_date) , 
				date_format( payment_date,  "%d - %b- %Y")  from  payment; 

-- group by 
-- total sales 
select sum(amount) from payment;

-- total sales of customer_id  =1

select sum(amount) from payment
where customer_id = 1;

select sum(amount) from payment

where customer_id in  (1,2,3);

-- distict 
select distinct(staff_id) from payment;

-- total unique customer 
select  count(distinct(customer_id)) from payment;

-- sale amount by staff id
select  staff_id,  sum(amount) from payment
group by staff_id
order by sum(amount);

select  customer_id,  sum(amount) from payment
group by customer_id 
order by sum(amount) desc;

select  customer_id,  sum(amount) as total  from payment
group by customer_id 
order by  total  desc
limit 5;

-- DML  21/03/25
-- insert , update, delete 
-- create a table 
--  coursre  --> c id, name , fee  -- pk 
-- students   id, name, course_id ,address  --  pk ,fK
-- insert data 3 students, 3 course data
create database class313;
use class313;
create table course (
		cid int primary key , 
        name varchar(50) , 
        fee float);

create table students (
				sid  int  primary key, 
                name varchar(100), 
                course_id int , 
                address varchar(100),
                foreign key (course_id) references course(cid)
                );
insert into course values
					( 1, "ds",3000), 
                    (2, "java", 2000),
                    (3, "python", 2000)
	;
insert into students values( 1, "deep",2, "delhi"), (2, "raj", 1, "noida"),(3, "arun", 1, "sector 15");

select * from students;
-- arun change the course python 
-- update
update students 
set  course_id = 2
where name="arun"  ;

update students 
set  course_id = 2 , address= "south ex"
where name="arun"  ;

insert into students values( 4, "alok",2, "delhi");
select * from students;

-- delete
delete from  students 
where sid= 4;

select * from course;

-- show the course name of  the students    -->2 -- > java
select * from students 
join course 
on students.course_id = course.cid;

 -- show the course name of  the students   
 select students.name ,cid,  course.name from students 
join course 
on students.course_id = course.cid;

-- show the course name of  deep    -->2 -- > java
 select students.name ,cid,  course.name from students 
join course 
on students.course_id = course.cid

where students.name= "deep";

desc students;


-- single line comments
/*
multilline comments  start with /*   -------- end with */ 
/*
sdfd

dsfd
sfddsd
*/
/*
Joins
A JOIN clause is used to combine rows from two or more tables, based on a related column between them.

Types of JOins 
	1. inner join
    2, left join 
    3. right joins
    4. self joins 
    5. cross joins
    6. full joins
*/
-- inner joins
 select students.name ,cid,  course.name from students 
inner join course 
on students.course_id = course.cid;

insert into students values( 4, "alok",null, "delhi");
select * from students;

-- left join 
 select *  from students 
left join course 
on students.course_id = course.cid;

-- Right join 
 select *  from students 
right join course 
on students.course_id = course.cid;

-- show only nulls
 select *  from students 
left join course 
on students.course_id = course.cid
where cid is null;

-- cross join 
 select  * from students 
cross join course ;
-- full join  union  ,, union all 
-- group by 
-- having 
-- existing
-- case
-- joins


-- optional 
-- MySQL IFNULL() Function
-- The MySQL IFNULL() function lets you return an alternative value if an expression is NULL.
-- The MySQL COALESCE() function returns the first non-null value in a list of expressions.
-- SELECT COALESCE(NULL, 'A', 'B', NULL); 
-- comments
-- single line 
-- multiline

-- The MySQL ANY and ALL Operators
