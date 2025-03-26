-- show the actor name and their movies name 
select  * from mavenmovies.actor;

use  mavenmovies;

select  actor.actor_id ,first_name, title from actor
join film_actor
on film_actor.actor_id = actor.actor_id
join film

on film_actor.film_id = film.film_id
;
-- show the customer wise payment
select customer_id , sum(amount) from payment
group by customer_id;


-- show the customer wise payment where total payment >200
select customer_id , sum(amount) a from payment
group by customer_id
having  a >=200;

-- show the customer wise payment where total payment  = max

select customer_id , sum(amount) a from payment
group by customer_id
order by a Desc
limit 2
offset 2;

-- show the customer wise payment where total payment  > avg
select customer_id , sum(amount) a from payment
group by customer_id
having  a >150;

-- avg 
select  * from payment;

select  avg(amount) from payment;

select  * from  payment 
where amount > 4.217695;

-- sub queries
select  * from  payment 
where amount >  (select  avg(amount) from payment);

-- sub queries
select  * from  payment 
where  customer_id in (select  customer_id  from customer) ;

-- 
select  customer_id  from customer;

-- -- Find the films  in the 'Action' genre.   
-- film category, category 
select * from film_category  
where category_id = ( select  category_id  from category  where name="action");


-- 
select * from category;

select film_id from film_category where category_id = (select category_id from category where name = 'Action');


-- multi row 
-- actor or actor id
-- show the actor award which last name  = DAVIS
 select actor_id from actor   where last_name= "DAVIS";
select * from actor_award
where actor_id  in (  select actor_id from actor   where last_name= "DAVIS") ;

select * from actor;
-- show   
-- multi column
--  multi columns sub query
-- show actor name who is also our customer 
select  * from actor
where (first_name , last_name)  in (select first_name , last_name  from customer);

-- non corelated
-- find  customer name  
select first_name from customer
where  customer_id in ( select  customer_id  from payment where customer.customer_id = payment.customer_id);

select  customer_id  from payment where customer.customer_id = payment.customer_id;

