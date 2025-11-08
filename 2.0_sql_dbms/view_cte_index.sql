-- view,index , CTE
-- 1. Index use for fast searching
-- CREATE INDEX index_name ON table_name (column1, column2, ...);
use mavenmovies;
create index abc on actor (first_name, last_name);

-- how to use index 
-- use as a normal query
select first_name from actor;

-- show all indexes
SHOW INDEXES FROM actor;

-- Delete the index
-- DROP INDEX index_name ON table_name;
Drop index abc on actor;

-- VIEW  create a virtual table on any query
-- syntax create view viewname  as qery
create view bottom as
select first_name, amt from customer 
		right join  
        (select customer_id,sum(amount) amt from payment
						group by customer_id
						order by amt
						limit 5) as t
		on customer.customer_id = t.customer_id;
-- use create  as normal table
select * from bottom;

-- CTE (COMMON TABLE EXPRESSION) 
-- create a temporary table and used after create a CTE
-- with CTE_name AS (query) , use as normal query
with xyz as (
select first_name, amt from customer 
		right join  
        (select customer_id,sum(amount) amt from payment
						group by customer_id
						order by amt Desc
						limit 5) as t
		on customer.customer_id = t.customer_id
) select * from xyz;

-- window functions
