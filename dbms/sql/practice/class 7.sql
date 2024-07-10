select curdate();
select date_add(now(), interval 1 hour );
select date_sub(now() , interval 3 hour);


select  now(), extract(year from now()) as year;

select  now() current, extract(month from now()) month;

select now() current,
extract(day from now()) day,
extract(month from now()) month,
extract(year from now()) as year,
extract(minute from now()) as minute,
extract(second from now()) as second ;
select second(now()), year(now());

select datediff('2024-05-30', '2024-05-21') AS date_difference;
select month('2024-01-01') - month ("2024-03-07");

use mavenmovies;
select  * from payment;

-- total sale in feb month 
select sum(amount) as feb_sale from payment
where month(payment_date) =02;

-- sale bw feb to jun
select sum(amount) as sale from payment
where month(payment_date)
between 2 and 6;

-- solve
select month(payment_date) from payment;

-- total sales in 2005


select  customer_id,amount from payment 
order by amount desc limit 5;

-- total sales ,min, max , count  of customer

-- avg
select avg(amount) from payment;

-- number of customers
select count(customer_id ) as no_of_customer from payment;

-- lowest price in amount
select min(amount) from payment;

-- highest price in amount
select max(amount) from payment;

-- group by 
select  customer_id , sum(amount), max(amount) from  payment
group by customer_id
order by sum(amount) desc;

-- group by with having
select  customer_id , sum(amount), max(amount) from  payment
group by customer_id
having sum(amount)>200
order by sum(amount) desc;

-- questions group by
use mavenmovies;

-- top 5 highest award winning actors
select first_name ,count(awards) as awards
from actor_Award
group by first_name
order by awards Desc
limit 5; 

-- actor win only 2 awards
select first_name ,count(awards) as awards
from actor_Award
group by first_name
having awards =2
order by awards Desc
;
select * from film;
-- having and group by conditions 
SELECT sum(rating), COUNT(*), length
FROM film 
GROUP BY length;

-- error
SELECT sum(rating),length , COUNT(*) 
FROM film 
GROUP BY rental_rate;

-- solution 
SELECT SUM(rating), length, COUNT(*)
FROM film
GROUP BY rental_rate, length;

-- joins 
select * from actor;

select * FROM ACTOR_AWARD;

--  inner joins use to show all columns
select * from 
actor 
inner join actor_Award 
on actor.actor_id = actor_Award.actor_id
;
--  inner joins use to show only first name from 
-- actor table and awards from actor award table 
select actor.first_name, actor_award.awards from 
actor 
inner join actor_Award 
on actor.actor_id = actor_Award.actor_id
;

-- use alias
select a.first_name, b.awards from 
actor a
inner join actor_Award b
on a.actor_id = b.actor_id
;

-- or use like as both same alias
-- use alias
select a.first_name, b.awards from 
actor as a
inner join actor_Award as b
on a.actor_id = b.actor_id
;

