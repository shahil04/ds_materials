-- Create `employees` Table
create database subquerydb;
use subquerydb;
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

SELECT 
    employee_id, 
    first_name, 
    last_name, 
    salary,
(select max(salary) from employees) as maxx,
((select max(salary) from employees)- salary) as difference
from employees;


SELECT first_name, last_name, salary
FROM employees
WHERE salary = (SELECT MAX(salary) FROM employees);

INSERT INTO employees (employee_id, first_name, last_name, department_id, salary) VALUES
(6, 'Joe', 'Doe', 101, 80000.00);

SELECT first_name, last_name
FROM employees
WHERE department_id IN (SELECT department_id FROM departments WHERE department_name = 'IT');

select * from employees;

SELECT employee_id, first_name, last_name, salary
FROM employees e
WHERE salary >= (SELECT AVG(salary) 
                FROM employees 
                WHERE department_id = e.department_id)
;