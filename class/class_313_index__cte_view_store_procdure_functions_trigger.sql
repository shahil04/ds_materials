-- Practice Questions on sub-query
	 -- Retrieve the titles of films that have a rental duration greater than the average rental duration of all films.
select * from film ;  -- step 1
select avg(rental_duration) from film;  -- step 2

select title from film 
where  rental_duration  > (select avg(rental_duration) from film);  -- combine 1 and 2

	-- Find the titles of films that are available in the inventory. 
select * from inventory;

select  title  from  film 
where  film_id in (select film_id from inventory); 

--  multi columns sub query
-- show actor name who is also our customer 
select  * from actor
where (first_name , last_name)  in (select first_name , last_name  from customer);




SELECT * ,first_name, last_name FROM actor 
WHERE (first_name, last_name) IN (SELECT first_name, last_name FROM customer );


-- index
-- Indexes are used to retrieve data from the database more quickly than otherwise. 
-- The users cannot see the indexes, they are just used to speed up searches/queries.
-- syntax
-- CREATE INDEX index_name
-- ON table_name (column1, column2, ...);

-- use first name as search 
create index  fname
on  actor (first_name);

-- how to use indexes  as usal 
select first_name from actor;

 -- CTE
select * from actor_award;

with cte1 as (
select  first_name as f ,last_name from actor)
select f from cte1;

with weekly_report as (
select  first_name as f ,last_name , awards from actor
join actor_award  )

select * from weekly_report;

--  views 
-- In SQL, a view is a virtual table based on the result-set of an SQL statement.
-- A view contains rows and columns, just like a real table. 
-- The fields in a view are fields from one or more real tables in the database.

-- CREATE VIEW view_name AS
-- SELECT column1, column2, ...
-- FROM table_name
-- WHERE condition;
create  view  view1  as (
select  first_name ,last_name , awards from actor
join actor_award);


select * from view1
where first_name  in ( select  first_name from customer)

