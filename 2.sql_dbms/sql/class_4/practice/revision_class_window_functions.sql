-- window functions
use class_11_1;
CREATE TABLE catagory (
    new_id INT,
    new_cat VARCHAR(50)
);


INSERT INTO catagory (new_id, new_cat) VALUES
(100, 'Agni'),
(200, 'Agni'),
(500, 'Dharti'),
(700, 'Dharti'),
(200, 'Vayu'),
(300, 'Vayu'),
(500, 'Vayu');

select * from your_table_name;

-- use window
select sum(new_id) from your_table_name;

select new_cat, sum(new_id) from your_table_name
group by new_cat;

-- i want the value in each row for compare each row with total value;
select  new_cat, new_id, sum(new_id) over() as total from your_table_name;  -- 

-- Show  the category-wise total and then compare  with it.
select new_cat, new_id, sum(new_id) over(partition by new_cat ) from your_table_name;

-- also include the total 
select new_cat, new_id, 
sum(new_id) over(partition by new_cat ) as category_total,
sum(new_id) over() as total from your_table_name;

-- sum , avg, min, max , count   aggrigate functions using in window 

select new_cat, new_id, 
sum(new_id) over(partition by new_cat ) as category_total,
sum(new_id) over() as total, 
avg(new_id) over(partition by new_cat) as cat_avg,
avg(new_id) over() as total_Avg,
count(new_id) over(partition by new_cat) as cat_wise_count,
count(new_id) over() as total_count
from your_table_name;

-- ranking funtions 
-- ROW_NUMBER, RANK, DENSE_RANK, PERCENT_RANK

-- row number provide a serail number 
select * , row_number() over() as sn_no from your_table_name;

-- row number in category-wise
select * , row_number() over(partition by new_cat) as cat_no,
row_number() over() as sn_no from your_table_name;

--  define the serial number based on new_id/amount value  
-- on all window as well as categories-wise partiotion
select * , row_number() over(order by new_id) as sn_no,
row_number() over(partition by new_cat order by new_id ) as cat_no 
from your_table_name;

-- 
-- rank , dense_rank  provide a serail number 
select * , row_number() over(order by new_id) as row_numbers,
rank()over(order by new_id) as ranks,
dense_rank() over(order by new_id) as d_rank,
percent_rank() over(order by new_id) as p_rank from your_table_name;

-- 
-- views
-- indexes 
-- cte



-- crerate view
create view window_func as
select new_cat, new_id, 
sum(new_id) over(partition by new_cat ) as category_total,
sum(new_id) over() as total, 
avg(new_id) over(partition by new_cat) as cat_avg,
avg(new_id) over() as total_Avg,
count(new_id) over(partition by new_cat) as cat_wise_count,
count(new_id) over() as total_count
from your_table_name;

select * from window_func;

-- COMMON TABLE EXPRESSION (CTE)
-- WITH

WITH MY_CTE (new_cat, new_id,category_total,total, cat_avg ,total_Avg) AS (
select new_cat, new_id, 
sum(new_id) over(partition by new_cat ) as category_total,
sum(new_id) over() as total, 
avg(new_id) over(partition by new_cat) as cat_avg,
avg(new_id) over() as total_Avg
from your_table_name )

SELECT new_cat, total FROM MY_CTE
where new_cat ="Agni";

-- indexes
 create index my_index on catagory( new_cat);
 
 select new_cat from catagory;
 