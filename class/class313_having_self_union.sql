-- self join 
-- union 
-- group by having 
-- case
-- if 



-- https://www.geeksforgeeks.org/mysql-self-join/
-- show the  name of the customer and the status of customer  product.
select  first_name , status from customers 
inner join shippings
on  customers.customer_id= shippings.customer;
-- show the customer name and item they buy
select  first_name , item from customers 
inner join orders
on  customers.customer_id= orders.customer_id;

-- more then 2 joins 
select  first_name ,item, status from customers 
inner join shippings
on  customers.customer_id= shippings.customer
inner join orders
on  customers.customer_id= orders.customer_id;
;

-- if order is pending set as a priority otherwise write successful

select  first_name ,item, status ,
case 
	when status="Pending" then "priority"
	else "successfull"
end  as current

from customers 
inner join shippings
on  customers.customer_id= shippings.customer
inner join orders
on  customers.customer_id= orders.customer_id;



-- if order is pending set as a priority otherwise write successful
select  first_name ,amount , 
case  
when amount <=350 then "Low"
when amount >350 and amount<=800 then "Medium"
else "High"
end  as customer_type

from customers
join orders
on customers.customer_id= orders.customer_id;


===============
CREATE TABLE employees (
    employee_id INT PRIMARY KEY,
    employee_name VARCHAR(50),
    manager_id INT,
    FOREIGN KEY (manager_id) REFERENCES employees(employee_id)
);

INSERT INTO employees VALUES (1, 'John', NULL);
INSERT INTO employees VALUES (2, 'Jane', 1);
INSERT INTO employees VALUES (3, 'Bob', 2);
INSERT INTO employees VALUES (4, 'Alice', 1);
INSERT INTO employees VALUES (5, 'Charlie', 3);



=== Group by and having
SELECT  awards   , count( awards) a FROM mavenmovies.actor_award
group by awards
having a >20
order by  a Desc;

SELECT  awards   , count( awards) a FROM mavenmovies.actor_award
group by awards
having a >20
order by  a Desc;