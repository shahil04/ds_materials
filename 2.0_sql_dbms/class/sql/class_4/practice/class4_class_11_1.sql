use mavenmovies;

show tables;

select * from actor;

-- rowwise conditions 
-- id = 1
select * from actor 
where actor_id =1;

-- last name MIRANDA
select * from actor 
where last_name ='miranda';

-- operators Arthematic 
-- +,-,*,/,%
select * from payment;

select payment_id ,amount, amount-0.5 from payment;

-- alias
-- with as 
select payment_id ,amount, amount-0.5 as actual_amount from payment;
-- without as 
select payment_id ,amount, amount-0.5 actual_amt from payment;

select payment_id ,amount, amount-0.5 actual_amt, amount*.20 as discount_20 from payment;

-- relational operators  >,<,>=,<=, != <>, 
-- <10 
select * from payment
where amount>10;

-- order by use
select * from payment
where amount>=10
order by amount;

-- change order in desc
select * from payment
where amount>=10
order by amount desc;

-- limit 5

select * from payment
where amount>=10
order by amount desc
limit 4;

-- logical operators
-- and or not 


-- show the details of customer_id 13 and amount >10;
select * from payment
where customer_id =13 and amount>10;

-- or 
select * from payment
where customer_id =13 or amount>10;

-- not
select * from payment
where customer_id <>2;

-- null 
select * from payment
where staff_id is null ;

select * from payment
where customer_id is not null;

-- aggrigate funtions 
-- min ,max , sum,avg, count

select sum(amount) from payment;

select avg(amount) from payment;

select sum(amount),avg(amount),min(amount), max(amount),count(amount) from payment;


-- like operator 
select * from actor;

select * from actor
where  first_name like 's%';

-- start s and only 4 char
select * from actor
where  first_name like 's___';

-- start any char and then S and multipule char
select * from actor
where  first_name like '_enn%';

-- find the details  actor_id 1 ,19,13 ,20
-- list  oprators (IN)
select * from actor 
where actor_id in (1,19,13,20);

-- range operators
select * from actor
where  actor_id between 20 and 30;

use mavenmovies;
 -- question   find the actor name stat with c and end with n ;
 select * from actor
 where first_name like "c%n";
 
 -- order by 
 
 -- group by 
 select * from payment;
 -- total pay by customer 3 
 select sum(amount) from payment
 where customer_id =3 ;
 
  -- total pay by customer 3  and how many times he/she pay 
 select count(customer_id) as repeat_pay, sum(amount) total_pay from payment
 where customer_id in (5,3);
 
 select * from payment;
 
 -- unique value from columns  using distinct
 select distinct(customer_id) from payment;
 
 -- The GROUP BY statement groups rows that have the same values into summary rows, like.

-- The GROUP BY statement is often used with aggregate functions (COUNT(), MAX(), MIN(), SUM(), AVG()) to group the result-set by one or more columns.

select customer_id, sum(amount) total 
from payment 
group by customer_id;

-- top paying customers 
select customer_id, sum(amount) total 
from payment 
group by customer_id
order by total desc;

-- top 5 customers
select customer_id, sum(amount) total 
from payment 
group by customer_id
order by total desc
limit 5;

-- who is the 3rd higest paying customer
select customer_id, sum(amount) total 
from payment 
group by customer_id
order by total desc
limit 1
offset 2;


-- show the result who's total payment is > 200
select customer_id, sum(amount) total 
from payment 
group by customer_id
having total >=200;

-- having is use  for  condition in group 

-- funtions 
-- date  -- day ,date, year, month, datediff ,monthname, Extract.

-- day  extract the day of date
select payment_date, day(payment_date) day ,month(payment_date) month, 
	monthname(payment_date) as MName, year(payment_date) year
    from payment;
    
-- extract 
select extract(month from payment_date) from payment;


-- monthly sales 
select monthname(payment_date) as month , sum(amount)
	from payment
    group by month;
    

select distinct(year(payment_date)) from payment;

-- 
select monthname(payment_date) as month , year(payment_date)year ,  sum(amount)
	from payment
    group by month ,year ;
     

--  >8 then high paying , <8 and >4 , medium paying , <4 low paying 
use mavenmovies;
select * from payment;
-- using case statement  for create new column based on conditions
select customer_id, amount,
	case
		when amount>8 then "high paying"
        when amount>4 and amount<8 then "medium paying"
        else "low paying"
	end as customer_segment
 from payment;
-- text funtion       
update tablename
set colname ="new value"
where null_col_name is null; 
-- concat funtions
select concat("class", 1),
	concat("class","-" ,1);

select *, concat(first_name," ", last_name) as full_name from actor;
select lower("HELLO") as lower;
select upper("hello") as upper;
select replace("Hello World", "World", "Universe") as repalce_string;
select "Hello World", substr("Hello World", 1,6) as sub_string;
select length("Hello World") as length_of_string;
select char_length("Hello World") AS character_length_of_string;