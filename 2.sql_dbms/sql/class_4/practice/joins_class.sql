use mavenmovies;

desc film;
-- What smallest rental duration ?
select min(rental_duration) from film;

-- What is the highest replacement cost amongst all the films
select max(replacement_cost) from film;

-- Display all films whose title length is greater than 10 characters
select title, length(title) from film where length(title) > 10;

-- Provide the count of unique ratings of films provided
select count(distinct(rating)) from film;

-- Display the list of first 4 cities which start and end with ‘a’
select * from city where city like "a%a" limit 4;

-- List the total sales amount for each customer in the database

select * from payment;

SELECT 
    customer_id, SUM(amount) AS total_amount
FROM
    payment
GROUP BY customer_id;

SELECT * FROM actor;
SELECT * FROM actor_award;

-- natural join 
SELECT *
FROM actor
NATURAL JOIN actor_award;

SELECT *
FROM actor
JOIN actor_award
on actor.actor_id = actor_award.actor_id;


-- left join

select *
from actor 
left join actor_award
on actor.actor_id = actor_award.actor_id
order by actor.actor_id;

-- right join
select *
from actor 
right join actor_award
on actor.actor_id = actor_award.actor_id
order by actor.actor_id;

select *
from actor 
full join actor_award
on actor.actor_id = actor_award.actor_id
order by actor.actor_id;

-- full join 
select *
from actor 
full join actor_award;

-- self join

select *
from actor 
right join actor_award
on actor.actor_id = actor_award.actor_id
order by actor.actor_id;

CREATE TABLE employees (
    employee_id INT PRIMARY KEY,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    manager_id INT
);

use mavenmovies;
CREATE TABLE employees (
    employee_id INT PRIMARY KEY,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    manager_id INT
);

INSERT INTO employees (employee_id, first_name, last_name, manager_id) VALUES
(1, 'John', 'Doe', NULL),        -- Top-level manager
(2, 'Jane', 'Smith', 1),
(3, 'Jim', 'Brown', 1),
(4, 'Jake', 'White', 2),
(5, 'Jill', 'Black', 2);

INSERT INTO employees (employee_id, first_name, last_name, manager_id) VALUES
(1, 'John', 'Doe', NULL),        -- Top-level manager
(2, 'Jane', 'Smith', 1),
(3, 'Jim', 'Brown', 1),
(4, 'Jake', 'White', 2),
(5, 'Jill', 'Black', 2);


select * from employees;

SELECT e.employee_id, e.first_name , m.first_name as manager
FROM employees e
LEFT JOIN employees m ON e.manager_id = m.employee_id
ORDER BY e.employee_id;

select * from employees;

SELECT *
FROM employees e
LEFT JOIN employees m ON e.manager_id = m.employee_id
ORDER BY e.employee_id;

-- cross join
select *
from actor 
cross join actor_award
on actor.actor_id = actor_award.actor_id
order by actor.actor_id;
