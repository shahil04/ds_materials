-- Create Database
CREATE DATABASE IF NOT EXISTS mydatabase;
USE mydatabase;

-- Create `employees` Table
CREATE TABLE employees (
    employee_id INT PRIMARY KEY,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    department_id INT,
    salary DECIMAL(10, 2)
);

-- Create `departments` Table
CREATE TABLE departments (
    department_id INT PRIMARY KEY,
    department_name VARCHAR(50)
);

-- Create `projects` Table
CREATE TABLE projects (
    project_id INT PRIMARY KEY,
    project_name VARCHAR(50),
    manager_id INT
);

-- Insert Data into `employees` Table
INSERT INTO employees (employee_id, first_name, last_name, department_id, salary) VALUES
(1, 'John', 'Doe', 101, 60000.00),
(2, 'Jane', 'Smith', 102, 75000.00),
(3, 'Alice', 'Johnson', 101, 50000.00),
(4, 'Bob', 'Lee', 103, 55000.00),
(5, 'Charlie', 'Brown', 102, 70000.00);

-- Insert Data into `departments` Table
INSERT INTO departments (department_id, department_name) VALUES
(101, 'HR'),
(102, 'IT'),
(103, 'Finance');

-- Insert Data into `projects` Table
INSERT INTO projects (project_id, project_name, manager_id) VALUES
(1001, 'Alpha', 2),
(1002, 'Beta', 3),
(1003, 'Gamma', 5);



select	* from  employees;
-- single row
SELECT first_name, last_name, salary
FROM employees
WHERE salary = (SELECT MAX(salary) FROM employees);


-- multiple row
-- Example: Find employees who work in the IT department.
select department_id from departments where department_name="IT";

select * from employees
where department_id = 
(select department_id from departments where department_name="IT");

-- Example: Find employees whose salary is greater than the average salary
-- of their respective departments.
select first_name, salary, department_id from employees where 
salary > ( select avg(salary) from employees);

select * from employees;


SELECT employee_id, first_name, last_name, salary, department_id
FROM employees e
WHERE salary > (SELECT AVG(salary) 
                FROM employees 
                WHERE department_id = e.department_id);
                
                
-- from subquery 
select e.first_name , d.department_id, d.department_name
from employees as e 
join departments as d 
on e.department_id =d.department_id;

select newtable.first_name, newtable.department_name
from
(select e.first_name, d.department_id, d.department_name
from employees as e 
join departments as d 
on e.department_id =d.department_id
) as newtable;