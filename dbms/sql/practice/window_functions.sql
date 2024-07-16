CREATE DATABASE sales_db;

USE sales_db;

CREATE TABLE sales (
    sales_id INT PRIMARY KEY,
    salesperson_id INT,
    sale_date DATE,
    sale_amount DECIMAL(10, 2)
);

INSERT INTO sales (sales_id, salesperson_id, sale_date, sale_amount) VALUES
(1, 101, '2023-01-01', 500.00),
(2, 102, '2023-01-02', 700.00),
(3, 101, '2023-01-03', 200.00),
(4, 103, '2023-01-04', 300.00),
(5, 101, '2023-01-05', 400.00),
(6, 102, '2023-01-06', 1000.00),
(7, 103, '2023-01-07', 600.00),
(8, 101, '2023-01-08', 700.00),
(9, 102, '2023-01-09', 300.00),
(10, 103, '2023-01-10', 800.00);


-- Example Query 1: Running Total of Sales
SELECT 
    salesperson_id,
    sale_date,
    sale_amount,
    SUM(sale_amount) OVER (PARTITION BY salesperson_id ORDER BY sale_date) AS running_total
FROM 
    sales;

-- Example Query 2: Rank Sales by Salesperson
SELECT 
    salesperson_id,
    sale_date,
    sale_amount,
    RANK() OVER (PARTITION BY salesperson_id ORDER BY sale_amount DESC) AS sales_rank
FROM 
    sales;


-- ---------------
USE sales_db;

CREATE TABLE demo_window (
    new_id INT,
    new_cat VARCHAR(50)
);

INSERT INTO demo_window (new_id, new_cat) VALUES
(100, 'Agni'),
(200, 'Agni'),
(500, 'Dharti'),
(700, 'Dharti'),
(200, 'Vayu'),
(300, 'Vayu'),
(500, 'Vayu');

--   
create database sales_performance_db;
USE sales_performance_db;

CREATE TABLE sales (
    sales_id INT PRIMARY KEY,
    salesperson_id INT,
    sale_date DATE,
    sale_amount DECIMAL(10, 2)
);

-- insert
INSERT INTO sales (sales_id, salesperson_id, sale_date, sale_amount) VALUES
(1, 101, '2023-01-01', 500.00),
(2, 102, '2023-01-02', 700.00),
(3, 101, '2023-01-03', 200.00),
(4, 103, '2023-01-04', 300.00),
(5, 101, '2023-01-05', 400.00),
(6, 102, '2023-01-06', 1000.00),
(7, 103, '2023-01-07', 600.00),
(8, 101, '2023-01-08', 700.00),
(9, 102, '2023-01-09', 300.00),
(10, 103, '2023-01-10', 800.00);

-- perform the query to calculate the running 
-- total of sales for each salesperson.

SELECT 
    salesperson_id,
    sale_date,
    sale_amount,
    SUM(sale_amount) OVER (PARTITION BY salesperson_id ORDER BY sale_date) AS running_total
FROM 
    sales;


-- ==============