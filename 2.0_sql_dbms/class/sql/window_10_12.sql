use mavenmovies;

select *, new_id,new_id from category_table
where new_id =200;

select date_format('2008-05-15 22:23:00', '%a %D %b %Y') 
as formatted_date ;

select *, sum(new_id) over() from category_table;

select *, sum(new_id) over(partition by new_cat) from category_table;

create view xyz as
select *, 
		sum(new_id) over(partition by new_cat) as cat_total  ,
		sum(new_id) over(partition by new_cat)- new_id as diff  
        from category_table;


select * from xyz;


with abc as
(select *, 
		sum(new_id) over(partition by new_cat) as cat_total  ,
		sum(new_id) over(partition by new_cat)- new_id as diff  
        from category_table)
select * from abc;
-- count ,max ,min avg,sum

select *, 
		sum(new_id) over(partition by new_cat order by new_cat) as cat_total  ,
		sum(new_id) over(partition by new_cat)- new_id as diff  
        from category_table;
        
select *, 
		sum(new_id) over(partition by new_cat order by new_cat) as cat_total  ,
		sum(new_id) over(partition by new_cat)- new_id as diff,
        count(new_id) over() as count_total,
        count(new_id) over(partition by new_cat) as count
        from category_table;
        
        
select *, 
		sum(new_id) over(partition by new_cat order by new_cat) as cat_total  ,
		sum(new_id) over(partition by new_cat)- new_id as diff,
        count(new_id) over() as count_total,
        count(new_id) over(partition by new_cat) as count,
        max(new_id) over(partition by new_cat) as max,
        min(new_id) over(partition by new_cat) as min
        from category_table;
        
        
select *, 
		sum(new_id) over(partition BY new_cat ROWS BETWEEN 1 PRECEDING AND 2 FOLLOWING) as cat_total  ,
        sum(new_id) over(partition BY new_cat ROWS BETWEEN unbounded PRECEDING AND unbounded FOLLOWING) as total ,
         sum(new_id) over(partition BY new_cat) as total2 ,
		sum(new_id) over(partition by new_cat)- new_id as diff
        from category_table;
        
-- ranking funtions

select *,
	row_number() over()
	from category_table;
        
select *,
	row_number() over(partition by new_cat) as row_num,
    rank() over(order by new_id) as ranks,
    rank() over(partition by new_cat) as ranks,
     rank() over(order by new_cat desc) as ranks_order
	from category_table;
    
select *,
	row_number() over(order by new_id) as row_num,
    rank() over(order by new_id) as ranks,
    dense_rank() over(order by new_id) as dense_ranks,
    percent_rank() over(order by new_id) as percent_ranks
    
	from category_table;

select * ,
	first_value(new_id) over() normal_1st,
	first_value(new_id) over(partition by new_cat) as cat_wise_1st,
    first_value(new_id) over(order by new_cat)
	from category_table;
    
select * ,
    LAST_VALUE(new_id) OVER( ORDER BY new_id) AS "LAST_VALUE normal",
    LAST_VALUE(new_id) OVER( partition BY new_cat) AS "LAST_VALUE cat-wise"
	from category_table;

SELECT *,
LEAD(new_id) OVER( ORDER BY new_id) AS "LEAD",
LEAD(new_id,3) OVER( ORDER BY new_id) AS "LEAD by 3",
LAG(new_id) OVER( ORDER BY new_id) AS "LAG"
from category_table;	
