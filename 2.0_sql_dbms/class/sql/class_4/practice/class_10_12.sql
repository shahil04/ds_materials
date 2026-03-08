use mavenmovies;
show tables;
describe actor;
-- IN 
-- actor table actor id 1,4,5,7,10
select * from actor 
where actor_id in ( 1,4,5,7,10);
select * from actor 
where first_name in ("cuba", "carmen");
-- between
-- actor table  actor id 20 to 40
select * from actor 
where actor_id between 20 and 40;

select * from actor 
where actor_id is not null;

select customer_id, amount,
case
	when amount> 8 then "Premium customer"
    when amount  4 then "avg customer"
    else "Cheap customer"
END as customer_qlty
from payment;
Error Code: 1064. You have an error in your SQL syntax; check the manual that corresponds to
 your MySQL server version for the 
 right syntax to use near '4 then "avg customer"     else "Cheap customer" END as customer_qlty from paymen' at line 4

-- like 
select * from actor 
where first_name like "_LL__";
-- where , limit, distinct, 
select * from actor limit 5; -- top 5

select * from actor 
where first_name like "L%"
order by actor_id desc limit 5; -- bottom 5
-- order by
-- limit
-- like 
select count(customer_id) from customer;
select count(*) from rental;
select * from rental order by customer_id;
select distinct( customer_id) from rental;
select count(distinct( customer_id)) from rental;

select count(distinct(customer_id)) from payment
where amount in (9.99);
select * from payment
where amount in (9.99);

select customer_id ,sum(amount) from payment
group by customer_id;
-- operators
-- group by
-- having 

-- operations - from , join , where , group by , having , select , order by , limit

-- String Function -- concatinate, lower, upper, length, trim 
select *, concat("     ",first_name , " ", last_name) as full_name from actor;

select *, concat(first_name , " ", last_name)as full_name, 
lower(first_name) ,substr(first_name,2,3) from actor;
select "abc" , substr("abcd", 2,1);

select "   abcd    " as val , trim("   abcd    ") as val;

select "    abc   ", substr("    abc   ",1,3), trim("    abc   ") , substr(trim("    abc   "),1,2);
-- Math Function  -- round,cell, floor, 
select  amount, ceil(amount) , floor(amount) ,round(amount, 1) from payment;
use mavenmovies;
-- Date  and time Function  -- now, date , month, year, day, min ,hr,se;
select payment_date, amount , month(payment_date),monthname(payment_date) from payment;

select monthname(payment_date), sum(amount) from payment
group by monthname(payment_date);
select now();

select  distinct(year(payment_date)) from payment;

select payment_date, amount ,extract(month from payment_date), month(payment_date),
monthname(payment_date), year(payment_date) from payment;

select monthname(payment_date), sum(amount) from payment
where year(payment_date) =2005
group by monthname(payment_date);

-- Comparison Functions 
-- Aggregate Function 
--  joins 
select * from payment;
select * from customer;

-- ==============================================================================================================
-- join -01/09/2024
select *
from payment 
inner join customer 
on payment.customer_id  =customer.customer_id;
-- 
select first_name, amount, customer.customer_id
from payment 
inner join customer 
on payment.customer_id  =customer.customer_id;

-- name total 
select first_name, sum(amount)
from payment 
inner join customer 
on payment.customer_id  =customer.customer_id
group by first_name;

--
select * from film;
select * from film_actor;
select * from actor;

select *, title , actor_id from film 
join film_actor 
on film.film_id =film_actor.film_id;

-- title or actor name
select title , film_actor.film_id, first_name from film 
join film_actor 
on film.film_id =film_actor.film_id

join actor
on actor.actor_id = film_actor.actor_id;
;

select first_name, count(first_name) from film 
join film_actor 
on film.film_id =film_actor.film_id
join actor
on actor.actor_id = film_actor.actor_id

group by first_name
having count(first_name)>50
order by  count(first_name) desc
limit 3-- 
;
use mavenmovies;

select actor.actor_id, first_name from actor 
union all
select actor_id, awards from actor_award;
 
select count(*) from actor 
cross  join 
actor_award;

select * from actor
join ;

select count(*) from actor_award;

select 200* 157;


-- self join 
select * from customer;
select * from customer
where last_name like "SMITH";

select t1.first_name, t2.last_name from customer as t1
inner join  customer as t2 ;

select title , ac.film_id as film_no from film
inner join film_actor as ac
on film.film_id =ac.film_id;



-- sub query
-- case expression 
-- CTE 
-- window functions 
-- index 
-- views