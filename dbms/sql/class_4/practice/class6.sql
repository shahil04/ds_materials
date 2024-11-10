use mavenmovies;

select title , rental_rate from film where rental_rate > 4  limit 5;

select * from film;

 -- string functions  concat,lower,upper,replace, substr, length, char_length
 
 select * from actor;
 
 select concat(first_name ,' ', last_name) as full_name from actor;
 select lower("HELLO WORLD") as name;
 select lower(first_name)  as name from actor;
 select upper("hello world1") as name;
 
-- replace
select replace("hello world" ,"hello", "hi") as new;

select  replace(last_name, last_name, "new" );

-- substring 
select substr("Hello world" ,6) as substring;
select substr("Hello world" ,1,6) ,length(substr("Hello world" ,1,6) ) as length;
select substr("Hello world" ,1,7) as substr ,length(substr("Hello world" ,1,7) ) as length;
use mavenmovies;
-- length
select last_name ,length(last_name)  from actor;
select last_name , length(last_name)as length , char_length(last_name) as char_length from actor; 
select "こんにちは" as name , length("こんにちは   ")as length , char_length("こんにちは   ") as char_length ; 

select "deep" name , length(name)as length , char_length(name) as char_length ;

SELECT ABS(-10) AS absolute_value;
select  ceil(4.2) ;
select floor(4.2);
select round(4.5);
select round(4.4);
select mod(10, 3);
select mod(3, 10);

select exp(2);

SELECT
    DATE_ADD(NOW(), INTERVAL 1 HOUR) AS added_one_hour,
    DATE_SUB(NOW(), INTERVAL 1 DAY) AS subtracted_one_day,
    EXTRACT(YEAR FROM NOW()) AS extracted_year,
    EXTRACT(MONTH FROM NOW()) AS extracted_month,
    EXTRACT(DAY FROM NOW()) AS extracted_day,
    EXTRACT(HOUR FROM NOW()) AS extracted_hour,
    EXTRACT(MINUTE FROM NOW()) AS extracted_minute,
    EXTRACT(SECOND FROM NOW()) AS extracted_second,
    DATEDIFF('2024-05-30', '2024-05-21') AS date_difference;

SELECT
    AVG(column_name) AS average_value,
    MAX(column_name) AS maximum_value,
    MIN(column_name) AS minimum_value,
    SUM(column_name) AS sum_of_values,
    COUNT(column_name) AS count_of_values
FROM table_name;

select count(*) from city
 group by city
 having country_id >10;

use mavenmovies;

SELECT  sum(rating),length , COUNT(*) 
FROM film
GROUP BY rental_rate;

SELECT SUM(rating), AVG(length) AS avg_length, COUNT(*)
FROM film
GROUP BY rental_rate;

SELECT SUM(rating), length, COUNT(*)
FROM film
GROUP BY rental_rate ;

SELECT SUM(rating), length, rental_rate, COUNT(*)
FROM film
GROUP BY rental_rate ,length;

SELECT (rating), AVG(length) AS avg_length, COUNT(*)
FROM film
GROUP BY rental_rate;

