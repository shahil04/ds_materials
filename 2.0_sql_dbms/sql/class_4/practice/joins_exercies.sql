create database e_commerce;
use e_commerce;

-- customer table
CREATE TABLE customers (
    customer_id INT PRIMARY KEY,
    customer_name VARCHAR(100),
    city VARCHAR(50)
);

INSERT INTO customers (customer_id, customer_name, city) VALUES
(1, 'Alice Johnson', 'New York'),
(2, 'Bob Smith', 'Los Angeles'),
(3, 'Charlie Brown', 'Chicago'),
(4, 'David Wilson', 'San Francisco'),
(5, 'Eva Green', 'New York'),
(6, 'Frank Wright', NULL),
(7, 'Grace Lee', 'Chicago'),
(8, 'Hannah White', 'Los Angeles'),
(9, 'Ian Thomas', 'New York'),
(10, 'Julia Black', NULL),
(11, 'Kevin Young', 'San Francisco'),
(12, 'Liam Scott', 'Boston'),
(13, 'Mia Martinez', 'Miami'),
(14, 'Noah Davis', 'Boston'),
(15, 'Olivia Perez', 'Miami'),
(16, 'Paul Adams', 'San Francisco'),
(17, 'Quinn Hall', 'Chicago'),
(18, 'Rachel Allen', 'Los Angeles'),
(19, 'Sam Harris', NULL),
(20, 'Tina Baker', 'New York');


-- create order table
CREATE TABLE orders (
    order_id INT PRIMARY KEY,
    customer_id INT,
    order_date DATE,
    order_amount DECIMAL(10, 2),
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

INSERT INTO orders (order_id, customer_id, order_date, order_amount) VALUES
(1, 1, '2024-01-01', 100.00),
(2, 2, '2024-01-02', 150.00),
(3, 1, '2024-01-03', 200.00),
(4, 3, '2024-01-04', 50.00),
(5, 5, '2024-01-05', 300.00),
(6, 6, '2024-01-06', 250.00),
(7, 8, '2024-01-07', 80.00),
(8, 9, '2024-01-08', 120.00),
(9, 10, '2024-01-09', 60.00),
(10, 12, '2024-01-10', 90.00),
(11, 13, '2024-01-11', 110.00),
(12, 14, '2024-01-12', 130.00),
(13, 15, '2024-01-13', 140.00),
(14, 16, '2024-01-14', 160.00),
(15, 17, '2024-01-15', 170.00),
(16, 18, '2024-01-16', 180.00),
(17, 20, '2024-01-17', 190.00),
(18, 3, '2024-01-18', 75.00),
(19, NULL, '2024-01-19', 85.00),
(20, NULL, '2024-01-20', 95.00);

--  Inner Join: Show all orders with customer details
SELECT 
    o.order_id,
    o.order_date,
    o.order_amount,
    c.customer_name,
    c.city
FROM 
    orders o
INNER JOIN 
    customers c ON o.customer_id = c.customer_id;

-- 2. Left Join: Show all customers and their orders, including those who haven't placed any orders
SELECT 
    c.customer_id,
    c.customer_name,
    o.order_id,
    o.order_date,
    o.order_amount
FROM 
    customers c
LEFT JOIN 
    orders o ON c.customer_id = o.customer_id;


 -- Right Join: Show all orders and their corresponding customers, including orders without customers (if any)
 
 SELECT 
    o.order_id,
    o.order_date,
    o.order_amount,
    c.customer_id,
    c.customer_name,
    c.city
FROM 
    orders o
RIGHT JOIN 
    customers c ON o.customer_id = c.customer_id;

-- 4. Self Join: Show customers living in the same city
SELECT 
    c1.customer_name AS customer1,
    c2.customer_name AS customer2,
    c1.city
FROM 
    customers c1
INNER JOIN 
    customers c2 ON c1.city = c2.city AND c1.customer_id <> c2.customer_id;

-- 5. Cross Join: Show all possible combinations of customers and orders
SELECT 
    c.customer_name,
    o.order_id,
    o.order_date,
    o.order_amount
FROM 
    customers c
CROSS JOIN 
    orders o;

-- use the CTE(common table Expressions) temporary
-- named result set created fromfromasimple SELECT statement
-- CTE define by With clause
with my_cte as (
	SELECT 
    c.customer_id,
    c.customer_name,
    o.order_id,
    o.order_date,
    o.order_amount
FROM 
    customers c
LEFT JOIN 
    orders o ON c.customer_id = o.customer_id
)
select * from my_cte;


select customer_name , order_Amount from my_cte;

-- Display the names of actors and the names of the films they have acted in.

use mavenmovies;
select * from  actor;
select * from film_actor;
select * from film;

select actor.first_name, film.title 
from actor 
inner join  film_actor
on film_actor.actor_id =actor.actor_id

inner join film
on film.film_id = film_actor.film_id

order by actor.actor_id;

-- grouping by actor_id 

select first_name ,count(*) 
from actor 
inner join  film_actor
on film_actor.actor_id =actor.actor_id

inner join film
on film.film_id = film_actor.film_id

group by first_name;