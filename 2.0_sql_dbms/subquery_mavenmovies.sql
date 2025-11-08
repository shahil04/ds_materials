-- Subquery
-- show the customer name who rent more then 150$,
-- customer  table
use mavenmovies;
select  first_name, sum(amount) as amt from customer 
			right join payment 
            on customer.customer_id =payment.customer_id
            group by first_name
            having amt>150
            order by amt desc
            limit 5;

-- average rental amout
select avg(amount) from payment;
-- show the payment details more then average. 
select * from payment where amount>4.2;

select * from payment where amount> (select avg(amount) from payment);

select customer_id,sum(amount) from payment
group by customer_id
order by sum(amount) desc
limit 1;
-- show the name of the customer who pay  max
-- subquery
select customer_id from payment
group by customer_id
order by sum(amount) desc
limit 1;


select * from customer where customer_id = 526;
-- single row subquery  Q 
select * from customer 
	where customer_id =(select customer_id from payment
						group by customer_id
						order by sum(amount) desc
						limit 1);
                        
-- Q. show the top 3 customer details 
select customer_id from payment
						group by customer_id
						order by sum(amount) desc
						limit 3;

-- multi row subquey  
select customer.customer_id,first_name from customer 
		right join  
        (select customer_id from payment
						group by customer_id
						order by sum(amount) desc
						limit 3) as t
		on customer.customer_id = t.customer_id;
        
-- multiple columns
--  show the lowest pay 5 customer name and amount
select customer_id,sum(amount) from payment
						group by customer_id
						order by sum(amount)
						limit 5;
 
select first_name, amt from customer 
		right join  
        (select customer_id,sum(amount) amt from payment
						group by customer_id
						order by amt
						limit 5) as t
		on customer.customer_id = t.customer_id;

-- show top 5 customer name using payment
-- show the 2nd highest paying customer


-- 2. Find films that are longer than the average length of all films.
-- Business idea: Identify films that take longer to watch than usual.
-- film
select avg(length) from film;

SELECT title, length from film where 
		length> (select avg(length) from film);

SELECT title,count(*) from film where 
		length> (select avg(length) from film);
-- 
SELECT COUNT(*)
FROM film f
WHERE f.length > (
    SELECT AVG(length)
    FROM film
);

-- Corelated Subquery
-- 3. Find customers who have rented more than 10 films. (customer, rental table)
-- Business idea: Identify top customers for loyalty offers.
select * from customer  
where (select count(*) from rental  where customer.customer_id = rental.customer_id) >10; 

-- select * from customer  
-- where value > 10




SELECT c.customer_id, c.first_name, c.last_name
FROM customer c
WHERE (
    SELECT COUNT(*)
    FROM rental r
    WHERE r.customer_id = c.customer_id
) > 10;

-- 4. Find films that have been rented at least once.-- inventory ,film
-- Business idea: Check which films are actually being watched.
select * from inventory;
select * from film;

select title ,count(*) as counts 
			from rental as r 
            join inventory as i
			on i.inventory_id = r.inventory_id
            inner join film
            on i.film_id = film.film_id 
			group by i.inventory_id
			having counts>0;



-- Hint: Use a correlated subquery with EXISTS.
SELECT f.film_id, f.title
FROM film f
WHERE EXISTS (
    SELECT 1
    FROM inventory i
    JOIN rental r ON i.inventory_id = r.inventory_id
    WHERE i.film_id = f.film_id
);

-- 1. Find customers who have rented at least one film from the same store they first registered at.
-- Business idea: Check if customers rent from their registration store.
SELECT c.customer_id, c.first_name, c.last_name
FROM customer c
WHERE EXISTS (
    SELECT 1
    FROM rental r
    JOIN inventory i ON r.inventory_id = i.inventory_id
    WHERE r.customer_id = c.customer_id
      AND i.store_id = c.store_id
);
