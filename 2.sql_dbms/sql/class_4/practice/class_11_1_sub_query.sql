-- sub query


-- find the customer id  who pay the max amount  -- subquery 
select * from payment;

-- single row
select max(amount) from payment;

-- without sub
select customer_id, amount from payment
where amount = 15;

-- non correlated single row subquery
select customer_id, amount from payment
where amount = (select max(amount) from payment);

-- find the all customer id who pay > then avgrage amount
select customer_id, amount from payment
where amount >= (select avg(amount) from payment);


-- find the most loyal customer id  only( one customer)
select customer_id, count(customer_id) as loyal from payment
group by customer_id
order by loyal desc
limit 1;


-- find the name of acotr who get the award  -- subquery 
select  actor_id from  actor_award;

select first_name, last_name from actor
where actor_id in (4,5,6,5);

-- multi row sub-query
select first_name, last_name from actor
where actor_id in (select  actor_id from  actor_award);

-- 
-- find the name of acotr and award name  --  correlated question

select first_name, last_name, (select awards from actor_award 
where actor.actor_id =actor_award.actor_id) as awards
from actor
where actor.actor_id in (select actor_id from actor_award);

-- show the customer name with total payment 
-- corelated sub query
select sum(amount) from payment;

select first_name , last_name, customer_id, 
	(select sum(amount) from payment 
    where payment.customer_id = customer.customer_id) 
    as total
    from customer;

-- cte, view , window , procedures 






select first_name, 
	last_name , customer_id,
	(select sum(amount) 
		from payment 
        where payment.customer_id= customer.customer_id) as total_pay
from customer ;

