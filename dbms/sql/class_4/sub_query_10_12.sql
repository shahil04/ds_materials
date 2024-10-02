-- self join
use mavenmovies; 
CREATE TABLE CUSTOMERS_self (
   ID INT NOT NULL,
   NAME VARCHAR (20) NOT NULL,
   AGE INT NOT NULL,
   ADDRESS CHAR (25),
   SALARY DECIMAL (18, 2),       
   PRIMARY KEY (ID)
);


INSERT INTO CUSTOMERS_self VALUES
(1, 'Ramesh', 32, 'Ahmedabad', 2000.00 ),
(2, 'Khilan', 25, 'Delhi', 1500.00 ),
(3, 'Kaushik', 23, 'Kota', 2000.00 ),
(4, 'Chaitali', 25, 'Mumbai', 6500.00 ),
(5, 'Hardik', 27, 'Bhopal', 8500.00 ),
(6, 'Komal', 22, 'Hyderabad', 4500.00 ),
(7, 'Muffy', 24, 'Indore', 10000.00 );


select * from  CUSTOMERS_self;

SELECT a.ID, b.NAME as EARNS_HIGHER, a.NAME 
as EARNS_LESS, a.SALARY as LOWER_SALARY
FROM CUSTOMERS_self as a join CUSTOMERS_self as b
WHERE a.SALARY < b.SALARY;


SELECT count(*)
FROM CUSTOMERS_self a join CUSTOMERS_self b
WHERE a.SALARY < b.SALARY;

SELECT count(*)
FROM CUSTOMERS_self a, CUSTOMERS_self b
WHERE a.SALARY < b.SALARY;


-- sub query 
select * from payment;

select * from payment
order by amount desc ;

select max(amount) from payment;

select * from payment 
where amount = 11.99;

select * from payment 
where amount = (select max(amount) from payment);

update payment set amount =15 where customer_id=13;

-- muliti row 
select * from actor;
select * from actor_award;

select * from actor_award
where actor_id in (38,5,12);


select actor_id from actor;
-- 
select * from actor_award
where actor_id in (select actor_id from actor);

-- multi column
select * from payment;

select customer_id ,amount from payment
where amount >5;

select * from payment
where (customer_id , amount) in (select customer_id ,amount from payment
where amount >5) ;

select customer_id ,sum(amount) from payment
group by customer_id;


select t from (select customer_id ,sum(amount) as t from payment
group by customer_id) as a
where t> 160;

-- 
-- Subquery in WHERE Clause: Find Films Released After the Oldest Film  -- film table

-- Subquery with IN: Find Customers Who Rented 'Comedy' Films -- joins and subqueries 
-- film ,  
select * from film 
where release_year > (select min(release_year) from film);
 
 -- Subquery in SELECT Clause: Find Total Payments Made by a Specific Customer - payment table, customer t
 
 select sum(amount) from payment 
 where customer_id =1;
 
 select first_name, last_name from customer 
 where customer_id =1;
 
  select first_name, last_name ,100 from customer 
 where customer_id =5;
 
  select first_name, last_name , ( select sum(amount) from payment 
 where customer_id =5) as total_pay from customer 
 where customer_id =5;
 
select first_name, 
	last_name , customer_id,
	(select sum(amount) 
		from payment 
        where payment.customer_id= customer.customer_id) as total_pay
from customer ;


select * from xyz;

-- CTE create 
with xyz  (first_name,total) as (
select first_name, 
	last_name , customer_id,
	(select sum(amount) 
		from payment 
        where payment.customer_id= customer.customer_id) as total_pay
from customer )

select first_name from xyz;

-- view
create view customer_total_pay as 
select first_name, 
	last_name , customer_id,
	(select sum(amount) as total
		from payment 
        where payment.customer_id= customer.customer_id) as total_pay
from customer;

select	* from customer_total_pay;  -- view work anywhere in file


select * from customer;
select * from xyz;  -- cte not run any where

 SELECT title
FROM film
WHERE release_year > (
    SELECT MIN(release_year)
    FROM film
);