use mavenmovies;
select  * from payment
order by  amount Desc;

select  customer_id, sum(amount) a from payment
group by customer_id 
order by  a Desc;
drop table  category_data;
CREATE TABLE category_data (
    new_id INT,
    new_cat VARCHAR(50) );
INSERT INTO category_data (new_id, new_cat) VALUES
(100, 'Agni'),
(200, 'Agni'),
(500, 'Dharti'),
(700, 'Dharti'),
(200, 'Vayu'),
(300, 'Vayu'),
(500, 'Vayu');
-- truncate table category_data;
Select * from category_data;


-- 
select  * , avg(new_id)   over() from category_data;

-- select  columns , functions  over() from table
select  new_cat , sum(new_id) from category_data
group by new_cat;


-- 
select  new_cat, new_id, sum(new_id)  over( partition by new_cat) as cat_total from category_data;

-- diffrence 
select  new_cat, new_id, 
					sum(new_id)  over( partition by new_cat) as cat_total,
					sum(new_id)  over( partition by new_cat) - new_id as diff
                    from category_data;
                    
-- all aggrigate functions

select  new_cat, new_id, 
					sum(new_id)  over( partition by new_cat) as cat_total,
					avg(new_id)  over( partition by new_cat) as avg,
                    count(new_id)  over( partition by new_cat) as count,
                    min(new_id)  over( partition by new_cat) as min,
                    max(new_id)  over( partition by new_cat) as max
                    from category_data;
                    
-- cat avg and total avg show 
select  new_cat, new_id, 
					avg(new_id)  over( ) as total_Avg,
					avg(new_id)  over( partition by new_cat) as avg
                     from category_data;
                     
-- Ranking Functions
-- row number , rank ,dense rank , percentile

-- row numbers 
select  
				row_number()  over( ) row_num, 
                new_cat, 
                new_id
                     from category_data;
-- rank 
select  
				row_number(  )  over(order by  new_id  ) row_num,
                rank()  over(  order by  new_id ) ranks, 
                dense_rank()  over(  order by  new_id ) dense_ranks,
                percent_rank()  over(  order by  new_id ) percentile_ranks,
                new_cat, 
                new_id
                     from category_data;

-- analytical function
-- lead ,leg, first, last
select  new_cat, 
			new_id,
            lead(new_id , 2) over () as leads,
            new_id - lead(new_id) over () as diff

		from category_data;

select  new_cat, 
			new_id,
            lead(new_id ) over () as leads,
            lag(new_id) over()  as lags,
            first_value(new_id) over(order by new_id ) as first,
            last_value(new_id) over( order by new_id) as last,
            last_value(new_id) over( order by new_id  rows  between  unbounded preceding and 0 following ) as last,
            last_value(new_id) over( order by new_id  rows  between  unbounded preceding  and unbounded following ) as last,
            last_value(new_id) over( order by new_id  rows  between  2 preceding and unbounded following ) as last,
            last_value(new_id) over( order by new_id  rows  between  2 preceding and 3 following ) as last
		from category_data;
        
-- https://learnsql.com/blog/define-window-frame-sql-window-functions/ 

