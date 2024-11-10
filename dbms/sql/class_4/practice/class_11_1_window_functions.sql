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


-- total the id
select sum(new_id) from catagory;

-- cataegory wise total 
select new_cat, sum(new_id) from catagory
group by new_cat;

select *, sum(new_id)over() as total  from catagory;   

select *, sum(new_id)over() as total  from catagory;   

-- We want the value in each row for compare each row with total value;
select new_cat, new_id, sum(new_id)over() as total  from catagory;  

-- Show  the category-wise total and then compare  with it.
select new_cat, new_id , 
	sum(new_id) over( partition by new_cat) as categoery_wise_total 
    from catagory;

-- with total
select new_cat, new_id , 
	sum(new_id)over() as total,
	sum(new_id) over(partition by new_cat) as categoery_wise_total 
    from catagory;
    
-- avg   (min ,max,count)
-- total avg and category_wise avg
-- count 

select new_cat, new_id , 
	sum(new_id)over() as total,
	sum(new_id) over(partition by new_cat) as categoery_wise_total ,
    avg(new_id) over() as total_avg,
    avg(new_id) over(partition by new_cat) as cat_avg,
    count(new_id) over(partition by new_cat) as cat_count,
    concat( (count(new_id) over(partition by new_cat))," ", new_cat) as counts
    from catagory;
    
    
-- row_number ,rank ,dense_rank, perct_rank
select *, row_number() over() serial_no from catagory;

-- define/ order the row number based on new_id value
select *, row_number() over(order by new_id) serial_no from catagory;

-- define/ order the row number based on new_id value and apply row_number in category_wise
select *, row_number() over( partition by new_cat order by new_id desc ) serial_no from catagory;

--
-- define/ order the row number based on new_id value
select *, row_number() over(order by new_id) row_num,
	rank() over(order by new_id) as ranks ,
    dense_rank() over(order by new_id) as dense_ranks,
    percent_rank() over(order by new_id) as p_rank
from catagory;


-- analytical funtions
-- lead lag, first, last
select *, first_value(new_id) over(order by new_id) row_num,
last_value(new_id) over(order by new_id) row_num,
lead(new_id ,2) over(order by new_id) row_num,
lag(new_id, 3) over(order by new_id) row_num
 
from catagory;

s