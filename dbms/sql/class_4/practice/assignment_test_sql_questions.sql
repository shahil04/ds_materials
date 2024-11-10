CREATE DATABASE salesdb1;
USE salesdb1 ;

CREATE TABLE students (
    student VARCHAR(50),
    student_id int;
    FirstName VARCHAR(50),
    LastName VARCHAR(50),
    Email VARCHAR(100),
    PhoneNumber VARCHAR(20),
    Address VARCHAR(100),
    City VARCHAR(50),
    State VARCHAR(50),
    ZipCode VARCHAR(10),
    Country VARCHAR(50),
    SignUpDate DATE
);

INSERT INTO studentns VALUES
(1, 'John', 'Doe', 'john.doe@example.com', '123-456-7890', '123 Elm St', 'Springfield', 'IL', '62701', 'USA', '2023-01-15'),
(2, 'Jane', 'Smith', 'jane.smith@example.com', '234-567-8901', '456 Oak St', 'Chicago', 'IL', '60601', 'USA', '2023-02-20'),
(3, 'Alice', 'Johnson', 'alice.johnson@example.com', '345-678-9012', '789 Pine St', 'Houston', 'TX', '77001', 'USA', '2023-03-10');

CREATE TABLE students (
    ProductID INT PRIMARY KEY,
    ProductName VARCHAR(100),
    Category VARCHAR(50),
    Price DECIMAL(10, 2),
    StockQuantity INT,
    SupplierID INT
);

INSERT INTO Products VALUES
(1, 'Laptop', 'Electronics', 999.99, 50, 1),
(2, 'Smartphone', 'Electronics', 599.99, 200, 2),
(3, 'Tablet', 'Electronics', 399.99, 150, 1);

CREATE TABLE Orders (
    OrderID INT PRIMARY KEY,
    CustomerID INT,
    OrderDate DATE,
    TotalAmount DECIMAL(10, 2),
    FOREIGN KEY (CustomerID) REFERENCES Customers(CustomerID)
);

INSERT INTO Orders VALUES
(1, 1, '2023-03-15', 1599.98),
(2, 2, '2023-04-10', 599.99),
(3, 3, '2023-05-05', 999.99);

CREATE TABLE OrderDetails (
    OrderDetailID INT PRIMARY KEY,
    OrderID INT,
    ProductID INT,
    Quantity INT,
    UnitPrice DECIMAL(10, 2),
    TotalPrice DECIMAL(10, 2),
    FOREIGN KEY (OrderID) REFERENCES Orders(OrderID),
    FOREIGN KEY (ProductID) REFERENCES Products(ProductID)
);

INSERT INTO OrderDetails VALUES
(1, 1, 1, 1, 999.99, 999.99),
(2, 1, 2, 1, 599.99, 599.99),
(3, 2, 2, 1, 599.99, 599.99),
(4, 3, 1, 1, 999.99, 999.99);

CREATE TABLE Reviews (
    ReviewID INT PRIMARY KEY,
    CustomerID INT,
    ProductID INT,
    Rating INT,
    ReviewDate DATE,
    Comments TEXT,
    FOREIGN KEY (CustomerID) REFERENCES Customers(CustomerID),
    FOREIGN KEY (ProductID) REFERENCES Products(ProductID)
);

INSERT INTO Reviews VALUES
(1, 1, 1, 5, '2023-03-20', 'Great laptop!'),
(2, 2, 2, 4, '2023-04-15', 'Good smartphone, but battery life could be better.'),
(3, 3, 1, 5, '2023-05-10', 'Excellent performance!');


-- 1.	Find all orders placed on '2023-04-10'.
SELECT *
FROM Orders
WHERE OrderDate = '2023-04-10';
-- 2.	Find the total quantity of each product sold.
SELECT ProductID, SUM(Quantity) AS TotalQuantitySold
FROM OrderDetails
GROUP BY ProductID;

-- 3.	List the names of customers who have placed an order with a total amount greater than $1000.

SELECT DISTINCT c.FirstName, c.LastName, o.TotalAmount
FROM Customers c
JOIN Orders o ON c.CustomerID = o.CustomerID
WHERE o.TotalAmount > 1000;

-- 4.	Get the average rating for each product.
SELECT ProductID, AVG(Rating) AS AverageRating
FROM Reviews
GROUP BY ProductID;
-- 5.	Find the most recent order date for each customer.
SELECT CustomerID, MAX(OrderDate) AS MostRecentOrderDate
FROM Orders
GROUP BY CustomerID;



-- 6.	Find the top 2 products with the highest total sales amount.
SELECT p.ProductName, SUM(od.TotalPrice) AS TotalSales
FROM OrderDetails od
JOIN Products p ON od.ProductID = p.ProductID
GROUP BY p.ProductName
ORDER BY TotalSales DESC
LIMIT 2;
select * from products;


-- 8.	Find all customers who have written more than one review.
SELECT CustomerID, COUNT(*) AS ReviewCount
FROM Reviews
GROUP BY CustomerID
HAVING ReviewCount > 1;


-- 9.	Get the average rating for products in each category.
SELECT p.Category, AVG(r.Rating) AS AverageRating
FROM Reviews r
JOIN Products p ON r.ProductID = p.ProductID
GROUP BY p.Category;


-- 10.	Find the customer who spent the most money on orders.
SELECT c.CustomerID, c.FirstName, c.LastName, SUM(o.TotalAmount) AS TotalSpent
FROM Customers c
JOIN Orders o ON c.CustomerID = o.CustomerID
GROUP BY c.CustomerID
ORDER BY TotalSpent DESC
LIMIT 1;

-- 11.	Get the list of products that were never ordered.
SELECT p.ProductID, p.ProductName
FROM Products p
LEFT JOIN OrderDetails od ON p.ProductID = od.ProductID
WHERE od.OrderDetailID IS NULL;


-- 9.	Retrieve the order details (including product name and quantity) for order ID 1.
SELECT p.ProductName, od.Quantity
FROM OrderDetails od
JOIN Products p ON od.ProductID = p.ProductID
WHERE od.OrderID = 1;


-- ---------------------------------

-- 1. Find all orders placed on '2023-04-10'.
SELECT *
FROM Orders
WHERE OrderDate = '2023-04-10';
-- 2. Find the total quantity of each product sold.
SELECT ProductID, SUM(Quantity) AS TotalQuantitySold
FROM OrderDetails
GROUP BY ProductID;

-- 3. List the names of customers who have placed an order with a total amount greater than $1000.

SELECT DISTINCT c.FirstName, c.LastName, o.TotalAmount
FROM Customers c
JOIN Orders o ON c.CustomerID = o.CustomerID
WHERE o.TotalAmount > 1000;

-- 4. Get the average rating for each product.
SELECT ProductID, AVG(Rating) AS AverageRating
FROM Reviews
GROUP BY ProductID;
-- 5. Find the most recent order date for each customer.
SELECT CustomerID, MAX(OrderDate) AS MostRecentOrderDate
FROM Orders
GROUP BY CustomerID;



-- 6.Find the top 2 products with the highest total sales amount.
SELECT p.ProductName, SUM(od.TotalPrice) AS TotalSales
FROM OrderDetails od
JOIN Products p ON od.ProductID = p.ProductID
GROUP BY p.ProductName
ORDER BY TotalSales DESC
LIMIT 2;
select * from products;


-- 7. Get the average rating for products in each category.
SELECT p.Category, AVG(r.Rating) AS AverageRating
FROM Reviews r
JOIN Products p ON r.ProductID = p.ProductID
GROUP BY p.Category;


-- 8.  Find the customer who spent the most money on orders.
SELECT c.CustomerID, c.FirstName, c.LastName, SUM(o.TotalAmount) AS TotalSpent
FROM Customers c
JOIN Orders o ON c.CustomerID = o.CustomerID
GROUP BY c.CustomerID
ORDER BY TotalSpent DESC
LIMIT 1;

-- 9. Find the name and email of the customer who placed the highest value order. (use subquery)
SELECT FirstName, LastName, Email
FROM Customers
WHERE CustomerID = (
    SELECT CustomerID
    FROM Orders
    ORDER BY TotalAmount DESC
    LIMIT 1
);

-- 10. Retrieve the order details (including product name and quantity) for order ID 1.
SELECT p.ProductName, od.Quantity
FROM OrderDetails od
JOIN Products p ON od.ProductID = p.ProductID
WHERE od.OrderID = 1;


-- ==========
SELECT *
FROM Orders
WHERE OrderDate = '2023-04-10';

-- 
SELECT p.ProductName, SUM(od.Quantity) AS TotalQuantitySold
FROM OrderDetails od
JOIN Products p ON od.ProductID = p.ProductID
GROUP BY p.ProductName;


SELECT c.FirstName, c.LastName
FROM Customers c
JOIN Orders o ON c.CustomerID = o.CustomerID
WHERE o.TotalAmount > 1000;

SELECT p.ProductName, AVG(r.Rating) AS AverageRating
FROM Reviews r
JOIN Products p ON r.ProductID = p.ProductID
GROUP BY p.ProductName;

--
SELECT c.CustomerID, c.FirstName, c.LastName, MAX(o.OrderDate) AS MostRecentOrderDate
FROM Customers c
JOIN Orders o ON c.CustomerID = o.CustomerID
GROUP BY c.CustomerID, c.FirstName, c.LastName;

SELECT p.ProductName, SUM(od.TotalPrice) AS TotalSales
FROM OrderDetails od
JOIN Products p ON od.ProductID = p.ProductID
GROUP BY p.ProductName
ORDER BY TotalSales DESC
LIMIT 2;


SELECT p.Category, AVG(r.Rating) AS AverageRating
FROM Reviews r
JOIN Products p ON r.ProductID = p.ProductID
GROUP BY p.Category;


SELECT c.CustomerID, c.FirstName, c.LastName, SUM(o.TotalAmount) AS TotalSpent
FROM Customers c
JOIN Orders o ON c.CustomerID = o.CustomerID
GROUP BY c.CustomerID, c.FirstName, c.LastName
ORDER BY TotalSpent DESC
LIMIT 1;


SELECT FirstName, LastName, Email
FROM Customers
WHERE CustomerID = (
    SELECT CustomerID
    FROM Orders
    ORDER BY TotalAmount DESC
    LIMIT 1
);


SELECT od.OrderID, p.ProductName, od.Quantity, od.UnitPrice, od.TotalPrice
FROM OrderDetails od
JOIN Products p ON od.ProductID = p.ProductID
WHERE od.OrderID = 1;


select * from products
where productname like '%S%';

