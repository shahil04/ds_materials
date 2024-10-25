-- joins
-- inner joins
use mavenmovies;
select * from actor;

-- alter 
alter table actor_award
drop column first_name, 
drop column last_name;

-- join 
select * from actor 
	inner join actor_award
	on actor.actor_id =actor_award.actor_id; -- common column relations
    
-- inner join 
--  show the actor name and award name ;
select actor.actor_id, first_name, last_name ,awards
	from actor
	inner join actor_award
	on actor.actor_id =actor_award.actor_id;

-- total actors
select count(*) from actor;

-- total actor 
select count(actor_award.actor_id)
	from actor
	inner join actor_award
	on actor.actor_id =actor_award.actor_id;


-- left join 
-- show the all actors details or the award name.
select first_name, last_name, awards
from actor
left join actor_award 
on actor.actor_id = actor_award.actor_id;

-- right join 
-- show all the actor name  who has winning awards
select * from actor_award;
select first_name, last_name, awards
from actor
right join actor_award 
on actor.actor_id = actor_award.actor_id;


-- payment table   and customer 
-- show name of customers along with amount 
select * from payment
inner join customer 
on payment.customer_id =customer.customer_id;

-- id, name , payment amount
select payment.customer_id, first_name, last_name, amount 
	from payment
	inner join customer 
	on payment.customer_id =customer.customer_id;

-- total pay by each customers with their customer id, name and total amount. -- group by 

select payment.customer_id, first_name, last_name, sum(amount) 
	from payment
	inner join customer 
	on payment.customer_id =customer.customer_id
    group by payment.customer_id;

-- multiple table join  more 2 table
 -- actor name with their moives name 
 select * from actor
 inner join film_actor
 on actor.actor_id =film_actor.actor_id
 
 inner join film 
 on film.film_id = film_actor.film_id; 


-- 
 select fa.actor_id, first_name, last_name, title 
	 from actor as a
	 inner join film_actor fa
	 on a.actor_id =fa.actor_id
	 inner join film f
	 on f.film_id = fa.film_id
     ; 

-- union
select first_name from actor
union 
select awards from actor_award;

select * from actor
cross join actor_award;