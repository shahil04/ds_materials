CREATE DATABASE mydb;
USE mydb;
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


-- Insert data into the 'country' table
INSERT INTO country (country_name) VALUES
('USA'), ('Canada'), ('Mexico');

-- Insert data into the 'city' table
INSERT INTO city (city_name, country_id) VALUES
('New York', 1),
('Los Angeles', 1),
('Toronto', 2),
('Vancouver', 2),
('Mexico City', 3);


DELIMITER //
CREATE PROCEDURE GetCityCountByCountry(IN country_name VARCHAR(100), OUT city_count INT)
BEGIN
    -- Select the count of cities for the given country
    SELECT COUNT(c.city_id) INTO city_count
    FROM city c
    INNER JOIN country co ON c.country_id = co.country_id
    WHERE co.country_name = country_name;
END //
DELIMITER ;

-- Declare a variable to hold the result
SET @city_count = 0;

-- Call the procedure for country 'USA'
CALL GetCityCountByCountry('Mexico', @city_count);

-- Select the value stored in the variable
SELECT @city_count;



-- Here’s a guide on how to create a stored procedure in MySQL from scratch, including the process of creating a database, tables, and a stored procedure. The example will include database creation, table creation, data insertion, and a stored procedure that performs a query.

-- ### Step-by-Step Guide

-- #### 1. **Create a Database**
-- The first step is to create a database in MySQL where the tables and stored procedures will reside.

-- ```sql
-- CREATE DATABASE mydb;
-- USE mydb;
-- ```

-- #### 2. **Create Tables**
-- Let's create two tables: `city` and `country`.

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
-- Now, let’s insert some sample data into the `country` and `city` tables.

-- ```sql
-- -- Insert data into the 'country' table
-- INSERT INTO country (country_name) VALUES
-- ('USA'), ('Canada'), ('Mexico');

-- -- Insert data into the 'city' table
-- INSERT INTO city (city_name, country_id) VALUES
-- ('New York', 1),
-- ('Los Angeles', 1),
-- ('Toronto', 2),
-- ('Vancouver', 2),
-- ('Mexico City', 3);
-- ```

-- #### 4. **Create a Stored Procedure**
-- We will now create a stored procedure that counts the number of cities in a given country.

-- ##### Stored Procedure Definition
-- - **Input parameter**: `IN country_name VARCHAR(100)` – This allows the user to pass the name of the country as an input.
-- - **Output parameter**: `OUT city_count INT` – This returns the number of cities in the specified country.

-- ```sql
-- DELIMITER //

-- CREATE PROCEDURE GetCityCountByCountry(IN country_name VARCHAR(100), OUT city_count INT)
-- BEGIN
--     -- Select the count of cities for the given country
--     SELECT COUNT(c.city_id) INTO city_count
--     FROM city c
--     INNER JOIN country co ON c.country_id = co.country_id
--     WHERE co.country_name = country_name;
-- END //

-- DELIMITER ;
-- ```

-- #### 5. **Calling the Stored Procedure**
-- You can now call the stored procedure by passing a country name and a variable to hold the result.

-- ```sql
-- -- Declare a variable to hold the result
-- SET @city_count = 0;

-- -- Call the procedure for country 'USA'
-- CALL GetCityCountByCountry('USA', @city_count);

-- -- Select the value stored in the variable
-- SELECT @city_count;
-- ```

-- ### Full Workflow Recap

-- 1. **Create Database**: The `mydb` database is created.
-- 2. **Create Tables**: Two tables, `city` and `country`, are created, with a foreign key relationship between them.
-- 3. **Insert Data**: Sample data is inserted into both tables to simulate real-world information.
-- 4. **Create Stored Procedure**: The stored procedure `GetCityCountByCountry` is defined, which counts how many cities are associated with a specific country.
-- 5. **Call Procedure**: The procedure is called by passing a country name, and the count of cities is returned.

-- ### Key Concepts in Stored Procedures:
-- - **IN parameter**: Accepts input values when calling the procedure.
-- - **OUT parameter**: Outputs a value from the procedure.
-- - **`DELIMITER` command**: Changes the statement delimiter so that MySQL doesn’t interpret semicolons inside the procedure as the end of the procedure.
--   
-- This basic example demonstrates how to create a stored procedure that interacts with multiple tables, performs an inner join, and returns a count.
