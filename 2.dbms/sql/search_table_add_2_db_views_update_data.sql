-- find DB name from table name 
SELECT table_schema, table_name
FROM information_schema.tables
WHERE table_name = 'Actor';

-- combine 2 tables from different database
SELECT * FROM mavenmovies.actor
UNION ALL
SELECT * FROM sakila.actor;


-- views dynamic update
-- Step 1: Create the 'sales' table
CREATE TABLE IF NOT EXISTS sales (
    id INT AUTO_INCREMENT PRIMARY KEY,
    product_name VARCHAR(100),
    quantity INT,
    price DECIMAL(10, 2)
);

-- Step 2: Insert data into the 'sales' table
INSERT INTO sales (product_name, quantity, price)
VALUES 
    ('Product A', 10, 20.50), 
    ('Product B', 5, 15.75);
select * from sales;
-- Step 3: Create a view 'all_sales' to display all sales data
CREATE OR REPLACE VIEW all_sales AS
SELECT * FROM sales;

select * from  all_sales;

-- Step 4: Insert additional data into the 'sales' table
INSERT INTO sales (product_name, quantity, price)
VALUES 
    ('Product C', 20, 30.00);

-- Step 5: Query the view to see all current data in the 'sales' table
SELECT * FROM all_sales;


-- In MySQL, views always display the latest data from the underlying tables without needing any manual updates. 
-- If data is added, updated, or deleted in the tables, querying the view will automatically reflect these changes.



-- INDEXS Automatic Index Updates
-- Step 1: Create a table with an index
CREATE TABLE sales (
    id INT AUTO_INCREMENT PRIMARY KEY,
    product_name VARCHAR(100),
    quantity INT,
    price DECIMAL(10, 2),
    INDEX (product_name)  -- Index on 'product_name'
);

-- Step 2: Insert data into the table
INSERT INTO sales (product_name, quantity, price)
VALUES ('Product A', 10, 20.50), 
       ('Product B', 5, 15.75),
       ('Product C', 20, 30.00);

-- Step 3: Check the index
SHOW INDEX FROM sales;

-- Step 4: Insert new data
INSERT INTO sales (product_name, quantity, price)
VALUES ('Product D', 8, 22.50);

-- Step 5: Run a query using the index
SELECT * FROM sales WHERE product_name = 'Product D';

-- Step 6: Update the table (index will automatically update)
UPDATE sales SET product_name = 'Product X' WHERE id = 4;

-- Step 7: Delete a row (index will automatically adjust)
DELETE FROM sales WHERE id = 3;

-- Step 8: Show the index again
SHOW INDEX FROM sales;
