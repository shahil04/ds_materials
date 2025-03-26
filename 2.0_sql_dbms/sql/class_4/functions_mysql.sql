-- MySQL CREATE FUNCTION Statement
-- A function is a block of organized, reusable code that is used to perform a single, related action. Functions provide better modularity for your application and a high degree of code reusing.

-- MySQL provides a set of built-in function which performs particular tasks for example the CURDATE() function returns the current date.

-- Syntax
-- Following is the syntax the CREATE FUNCTION statement −
-- CREATE FUNCTION function_Name(input_arguments) RETURNS output_parameter
-- Where, function_name is the name of the function you need to create, input_arguments are the input values of the function and output_parameter is the return value of the function.

CREATE DATABASE mydb2;
USE mydb2;
CREATE TABLE country (
    country_id INT AUTO_INCREMENT PRIMARY KEY,
    country_name VARCHAR(100) NOT NULL
);

CREATE TABLE city (
    city_id INT AUTO_INCREMENT PRIMARY KEY,
    city_name VARCHAR(100) NOT NULL,
    country_id INT,
    FOREIGN KEY (country_id) REFERENCES country(country_id)
);


-- Insert data into 'country' table
INSERT INTO country (country_name) VALUES
('USA'), ('Canada'), ('Mexico');

-- Insert data into 'city' table
INSERT INTO city (city_name, country_id) VALUES
('New York', 1),
('Los Angeles', 1),
('Toronto', 2),
('Vancouver', 2),
('Mexico City', 3);



DELIMITER //
CREATE FUNCTION GetCityCount(country_name VARCHAR(100))
RETURNS INT
DETERMINISTIC
BEGIN
    DECLARE city_count INT;

    -- Query to count the number of cities for a given country
    SELECT COUNT(c.city_id) INTO city_count
    FROM city c
    INNER JOIN country co ON c.country_id = co.country_id
    WHERE co.country_name = country_name;

    -- Return the result
    RETURN city_count;
END //
DELIMITER ;

-- call

-- Call the function to get the count of cities for the 'USA'
SELECT GetCityCount('USA') AS city_count;

-- You can use the function in more complex queries
SELECT country_name, GetCityCount(country_name) AS city_count
FROM country;




-- 

-- In MySQL, a **function** is similar to a stored procedure but is primarily used to return a single value. Functions can be used in SQL statements like `SELECT` or `INSERT`, and they must always return a value. Unlike procedures, functions cannot modify data (i.e., they cannot use `INSERT`, `UPDATE`, `DELETE`, or `CREATE` statements).

-- Here’s a step-by-step guide on how to create a user-defined function (UDF) in MySQL from scratch, similar to how you would create a procedure.

-- ### Steps to Create a Function in MySQL

-- #### 1. **Create a Database**
-- If you don’t already have a database, create one to work with.

-- ```sql
-- CREATE DATABASE mydb;
-- USE mydb;
-- ```

-- #### 2. **Create Tables**
-- We will create two tables, `city` and `country`, similar to the previous procedure example.

-- ```sql
-- CREATE TABLE country (
--     country_id INT AUTO_INCREMENT PRIMARY KEY,
--     country_name VARCHAR(100) NOT NULL
-- );

-- CREATE TABLE city (
--     city_id INT AUTO_INCREMENT PRIMARY KEY,
--     city_name VARCHAR(100) NOT NULL,
--     country_id INT,
--     FOREIGN KEY (country_id) REFERENCES country(country_id)
-- );
-- ```

-- #### 3. **Insert Sample Data**
-- Populate the `country` and `city` tables with sample data.

-- ```sql
-- -- Insert data into 'country' table
-- INSERT INTO country (country_name) VALUES
-- ('USA'), ('Canada'), ('Mexico');

-- -- Insert data into 'city' table
-- INSERT INTO city (city_name, country_id) VALUES
-- ('New York', 1),
-- ('Los Angeles', 1),
-- ('Toronto', 2),
-- ('Vancouver', 2),
-- ('Mexico City', 3);
-- ```

-- #### 4. **Create a Function**

-- We will create a function that returns the number of cities for a given country name. Unlike a procedure, the function will return a value directly.

-- ##### Function Definition:
-- - **Input parameter**: The function will take one input parameter, `country_name`.
-- - **Return type**: The function will return an `INT`, representing the number of cities in the given country.

-- ```sql
-- DELIMITER //

-- CREATE FUNCTION GetCityCount(country_name VARCHAR(100))
-- RETURNS INT
-- DETERMINISTIC
-- BEGIN
--     DECLARE city_count INT;

--     -- Query to count the number of cities for a given country
--     SELECT COUNT(c.city_id) INTO city_count
--     FROM city c
--     INNER JOIN country co ON c.country_id = co.country_id
--     WHERE co.country_name = country_name;

--     -- Return the result
--     RETURN city_count;
-- END //

-- DELIMITER ;
-- ```

-- ### Explanation:

-- - **`DELIMITER //`**: We change the delimiter to avoid conflicts with semicolons used inside the function.
-- - **`RETURNS INT`**: This specifies that the function returns an integer.
-- - **`DETERMINISTIC`**: This means the function always returns the same result for the same inputs (i.e., it is deterministic).
-- - **`RETURN`**: The function must return a value, unlike procedures.

-- #### 5. **Calling the Function**

-- You can now call the function in SQL statements, such as in `SELECT` statements.

-- ```sql
-- -- Call the function to get the count of cities for the 'USA'
-- SELECT GetCityCount('USA') AS city_count;

-- -- You can use the function in more complex queries
-- SELECT country_name, GetCityCount(country_name) AS city_count
-- FROM country;
-- ```

-- ### Key Differences Between Stored Procedures and Functions:
-- 1. **Return Value**: A function **must** return a single value, while a procedure does not have to return anything.
-- 2. **Use in Queries**: Functions can be called within SQL queries (`SELECT`, `WHERE`, etc.), while procedures must be invoked with the `CALL` statement.
-- 3. **Modifying Data**: Functions cannot modify data in the database (e.g., via `INSERT`, `UPDATE`, or `DELETE` statements), while procedures can.
-- 4. **Parameters**: Functions can only have `IN` parameters, while procedures can have `IN`, `OUT`, and `INOUT` parameters.

-- #### 6. **Modifying and Dropping a Function**

-- If you need to modify the function, you can drop it and recreate it:

-- ```sql
-- DROP FUNCTION IF EXISTS GetCityCount;

-- -- Then recreate the function as needed
-- ```

-- ### Summary:
-- 1. **Create Database**: Created `mydb` as the database.
-- 2. **Create Tables**: Created two tables, `city` and `country`, with a foreign key relationship.
-- 3. **Insert Data**: Inserted sample data into the tables.
-- 4. **Create Function**: Created a function `GetCityCount` to count the number of cities for a given country.
-- 5. **Call Function**: Called the function in `SELECT` statements to retrieve the city count.

-- This approach demonstrates how you can create and use MySQL functions to perform tasks that return a single value, which can then be used in other queries.