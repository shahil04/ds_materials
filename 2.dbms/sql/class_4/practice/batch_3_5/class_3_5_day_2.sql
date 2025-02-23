use mavenmovies;
-- -------------
select * from country; -- country data
select * from city; --

select * from address; -- postal codes 

select country, city, postal_code from city 
join address on city.city_id = address.city_id
join country on country.country_id = city.country_id
where country.country="India" and city="Bhopal";

-- views
create view ccp as
select city.country_id, city, postal_code from city 
join address on city.city_id = address.city_id;


select * from ccp;
select * from country;

select city, postal_code,country from ccp 
join country  on ccp.county_id =country.county_id
where country="India";

drop view ccp;

create view ccp as
select city.country_id, city.city_id ,city, postal_code from city 
join address on city.city_id = address.city_id;

-- 02/09/24
-- case statement
use mavenmovies;
select * from payment;

select customer_id, amount,
case
	when amount> 8 then "Premium customer"
    when amount > 4 then "avg customer"
    else "Cheap customer"
END as customer_qlty

FROM payment;

select avg(amount) from payment;
select * from payment;

select * from  payment 
where amount >(select avg(amount) from payment)  ;
-- 
select amount from  payment 
where amount >(select avg(amount) from payment)  ;

-- - 
select distinct(customer_id) from payment;

select first_name, last_name from customer;

select first_name, last_name from customer
where customer_id in (1,2,34);

-- 
select first_name, last_name from customer
where customer_id in (select distinct(customer_id) from payment);


select actor_id, film_id from film_actor;

select	 first_name , last_name from actor
where actor_id not in (select distinct(actor_id) from film_actor);


select customer_id, count(customer_id) from payment 
 group by customer_id
 HAVING count(customer_id)>5;

-- 
SELECT COUNT(*) FROM payment WHERE payment.customer_id = customer.customer_id > 5;

SELECT first_name, last_name FROM customer
WHERE (SELECT COUNT(*) FROM payment WHERE payment.customer_id = customer.customer_id) > 5;
use mavenmovies;

-- SELECT a.ename, a.deptno, a.sal
-- FROM emp a
-- WHERE (deptno, sal)  IN  (SELECT deptno, sal
-- FROM emp);

select  customer_id,rental_id from payment;

select * from payment
where customer_id= 1 and rental_id=76;

select * from payment
where (customer_id, rental_id) = (1,76);

select  customer_id,rental_id from payment;

select * from payment
where (customer_id,rental_id) IN (select  customer_id,rental_id from payment);


select * from payment;
-- ----------------------------------------------------------
/* Email Campaigns for customers of Store id 2
First, Last name and Email address of customers from Store id 2*/

/* movie with rental rate of 0.99$*/
select title, rental_rate from film where rental_rate>0.99;
/* we want to see rental rate and how many movies are in each rental rate categories*/
select rental_rate ,count(title) from film 
group by rental_rate;

/*Which rating do we have the most films in?*/
select rating ,count(*) from film group by rating;--  
/* List of films by Film Name, Category, Language*/

/* How many times each movie has been rented out? */

/*Revenue per Movie */

/* Most Spending Customer so that we can send him/her rewards or debate points*/

/* What Store has historically brought the most revenue */

/* Rentals per Month (such Jan => How much, etc)*/

/* Which date first movie was rented out ? */

/* Which date last movie was rented out ? */

/* Number of Rentals in Comedy , Sports and Family */

/*Users who have been rented at least 3 times*/

/*How much revenue has one single store made over PG13 and R rated films*/

/* Email Campaigns for customers of Store 2
First, Last name and Email address of customers from Store 2*/
SELECT first_name, last_name,email
FROM customer
WHERE store_id = 2;

/* movie with rental rate of 0.99$*/
SELECT COUNT(*) FROM film
WHERE rental_rate = 0.99;
use mavenmovies;

/* we want to see rental rate and how many movies are in each rental rate categories*/
SELECT rental_rate, COUNT(*) AS total_number_of_movies
FROM film
GROUP BY rental_rate;

/*Which rating do we have the most films in?*/
SELECT rating,COUNT(*) AS total_number_of_movies
FROM film
GROUP BY 1;


/* List of films by Film Name, Category, Language*/
SELECT f.title,c.name,l.name
FROM film f
JOIN film_category fc ON fc.film_id = f.film_id
JOIN category c ON fc.category_id = c.category_id
JOIN language l ON l.language_id = f.language_id;

/* How many times each movie has been rented out? */
SELECT i.film_id, f.title, COUNT(i.film_id) AS total_number_of_rental_times
FROM rental r
JOIN inventory i ON r.inventory_id = i.inventory_id
JOIN film f ON f.film_id = i.film_id
GROUP BY i.film_id
ORDER BY 3 DESC;

/*Revenue per Movie */
SELECT i.film_id, f.title, COUNT(i.film_id) AS total_number_of_rental_times, f.rental_rate, COUNT(i.film_id)*f.rental_rate AS revenue_per_movie
FROM rental r
JOIN inventory i ON r.inventory_id = i.inventory_id
JOIN film f ON f.film_id = i.film_id
GROUP BY i.film_id
ORDER BY 5 DESC;

/* Most Spending Customer so that we can send him/her rewards or debate points*/
SELECT c.customer_id, SUM(p.amount) AS "Total Spending"
FROM customer c
JOIN payment p ON c.customer_id = p.customer_id
GROUP BY 1
ORDER BY 2 DESC;

/* What Store has historically brought the most revenue */
SELECT s.store_id, SUM(p.amount) AS "Total Spending"
FROM store s
JOIN inventory i ON i.store_id = s.store_id
JOIN rental r ON r.inventory_id = i.inventory_id
JOIN payment p ON p.rental_id = r.rental_id
GROUP BY 1
ORDER BY 2 DESC;

/* Rentals per Month (such Jan => How much, etc)*/
SELECT date_format(rental_date,"%M") AS "Month", COUNT(*)
FROM rental
GROUP BY 1
ORDER BY 2 DESC;

/* Which date first movie was rented out ? */
SELECT MIN(rental_date)
FROM rental;

/* Which date last movie was rented out ? */
SELECT MAX(rental_date)
FROM rental;

/* Number of Rentals in Comedy , Sports and Family */
SELECT c.name, COUNT(c.name) AS "Number of Rentals"
FROM film f
JOIN film_category fc ON fc.film_id = f.film_id
JOIN category c ON c.category_id = fc.category_id
JOIN inventory i ON f.film_id = i.film_id
JOIN rental r ON r.inventory_id = i.inventory_id
WHERE c.name IN ("Comedy", "Sports", "Family")
GROUP BY 1;

/*Users who have been rented at least 3 times*/
SELECT c.customer_id, CONCAT(c.first_name, " ", c.last_name) AS "Customer Name", COUNT(c.customer_id) AS "Total Rentals"
FROM customer c
JOIN rental r ON c.customer_id = r.customer_id
GROUP BY 1
HAVING COUNT(c.customer_id) >= 3
ORDER BY 1;

/*How much revenue has one single store made over PG13 and R rated films*/
SELECT s.store_id, f.rating, SUM(p.amount) AS "Total Revenue"
FROM store s 
JOIN inventory i ON i.store_id = s.store_id
JOIN rental r ON r.inventory_id = i.inventory_id
JOIN payment p ON p.rental_id = r.rental_id
JOIN film f ON f.film_id = i.film_id
WHERE f.rating IN ("PG-13", "R")
GROUP BY 1,2;
