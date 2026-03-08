select amount, sum(amount) over() as total from payment;

select customer_id, amount,
		 row_number() over(order by payment_id),
         rank() over(order by payment_id),
		sum(amount) over(partition by customer_id) as customer_total ,
        sum(amount) over() as total,
        count(amount) over()
        from payment
        
        ;
        
-- Comparing Values: LAG() and LEAD() retrieve values from preceding or succeeding rows within the same partition.
-- Ranking: ROW_NUMBER(), RANK(), DENSE_RANK(), p ranka assign ranks to rows within a partition

-- The key component of a window function is the OVER clause, which defines this window of rows. The OVER clause can include:
-- PARTITION BY: Divides the result set into partitions (groups) based on specified columns. The window function is then applied independently to each partition.
-- ORDER BY: Defines the order of rows within each partition, which is crucial for functions that depend on the sequence of rows (e.g., ranking functions, running totals).
-- ROWS or RANGE clause: Further refines the window within a partition, specifying a frame of rows relative to the current row (e.g., "the previous 3 rows and the current row").