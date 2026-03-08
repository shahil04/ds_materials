-- Create Database
CREATE DATABASE IF NOT EXISTS mydatabase;
USE mydatabase;

-- Create `employees` Table
CREATE TABLE employees (
    employee_id INT PRIMARY KEY,
    first_name CHAR,
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

ALTER table employees 
modify first_name varchar(100);
-- Insert Data into `employees` Table
INSERT INTO employees (employee_id, first_name, last_name, department_id, salary) 
VALUES
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



-- employees;Get the highest salary among all employees and display it along with each employee's details.

SELECT 
    employee_id, 
    first_name, 
    last_name, 
    salary, 
    (SELECT MAX(salary) FROM employees) AS highest_salary
FROM employees;

-- Find the employee whose salary is the highest.
SELECT first_name, last_name, salary
FROM employees
WHERE salary = (SELECT MAX(salary) FROM employees);

-- Find employees who work in the IT department.
SELECT first_name, last_name
FROM employees
WHERE department_id IN (SELECT department_id FROM departments WHERE department_name = 'IT');

SELECT department_id FROM departments WHERE department_name = 'IT';

SELECT department_name FROM departments
where exists (select 101);

SELECT student_id 
FROM students 
WHERE EXISTS 
(SELECT 1 FROM enrollments WHERE 
students.student_id = enrollments.student_id);


create table demo (
demoid int,
name char);

 -- char  store only single charactors;
insert into demo value (1, 2);
insert into demo value (2, 's')DELIMITER $$

CREATE PROCEDURE GetHighestSalaryPerDepartment()
BEGIN
    SELECT e.department_id, d.department_name, e.employee_id, e.first_name, e.last_name, e.salary
    FROM employees e
    JOIN departments d ON e.department_id = d.department_id
    WHERE e.salary = (SELECT MAX(salary) FROM employees WHERE department_id = e.department_id
);
END$$

DELIMITER ;
;

CALL GetHighestSalaryPerDepartment();

-- create the trigger 
-- 1. Create the Audit Table
-- First, we need an audit table to store the salary change logs.

CREATE TABLE salary_audit (
    audit_id INT AUTO_INCREMENT PRIMARY KEY,
    employee_id INT,
    old_salary DECIMAL(10, 2),
    new_salary DECIMAL(10, 2),
    change_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- create trigger

DELIMITER $$

CREATE TRIGGER before_salary_update
BEFORE UPDATE ON employees
FOR EACH ROW
BEGIN
    IF OLD.salary <> NEW.salary THEN
        INSERT INTO salary_audit (employee_id, old_salary, new_salary)
        VALUES (OLD.employee_id, OLD.salary, NEW.salary);
    END IF;
END$$

DELIMITER ;

-- Using the Trigger
-- After creating the trigger, any update to the salary field in the employees table will automatically create an entry in the salary_audit table.
UPDATE employees
SET salary = 65000.00

WHERE employee_id = 1;

SELECT * FROM salary_audit;
