use mavenmovies;

select * from category_table;

select *, sum(new_id) over() from category_table;

select *, sum(new_id) over(partition by new_cat) from category_table;

select *, 
		sum(new_id) over(partition by new_cat) as cat_total  ,
		sum(new_id) over(partition by new_cat)- new_id as diff  
        from category_table;
        
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
		sum(new_id) over(partition by new_cat)- new_id as diff
        from category_table;
        
-- ranking funtions

select *,row_number() over()
	from category_table;
        
select *,
	row_number() over(partition by new_cat) as row_num,
    rank() over(order by new_id) as ranks,
    rank() over(partition by new_cat) as ranks
	from category_table;
    
select *,
	row_number() over(partition by new_cat) as row_num,
    rank() over(order by new_id) as ranks,
    dense_rank() over(order by new_id) as dense_ranks,
    percent_rank() over(order by new_id) as percent_ranks
    
	from category_table;

