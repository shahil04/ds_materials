select title from film;
select * from film_actor;

select * from actor
left outer join film_actor on actor.actor_id=film_actor.actor_id;

select last_name,first_name from actor
group by actor_id
having actor_id in (23,45,6,7,8) and last_name like "k%";

select * from customer;

select first_name ,datediff(last_update, create_date) as days_works from customer;

select  first_name , create_date,day(create_date), (select extract(year from create_date)),
(select count(amount) from payment)as pay ,
(select extract(day from create_date)),
dayofweek(create_Date) as day,
(select extract(HOUR_MICROSECOND from create_date)) as seconds
from customer;
use mavenmovies;
select * from customer; 
desc customer;

select current_date();

select * from actor;
select * from actor_award;

select * from actor_award 
inner join actor on actor.actor_id=actor_award.actor_id;

-- scaler subquery
select * from payment;
SELECT first_name, (SELECT MAX(amount) FROM payment) AS max_value
FROM customer;

-- single row

select * from country; -- country data
select * from city; -- city data
select * from address; -- postal codes 

-- Display all the cities with there postal code in India ?
    address
        INNER JOIN
    city ON address.city_id = city.city_id
        INNER JOIN
    country ON city.country_id = country.country_id
WHERE
    country = 'India';

select postal_code, city , country
from address 
inner join city on address.city_id = city.city_id

inner join country
on city.country_id = country.country_id

where country='india';

-- Display the names of actors and the names of the films they have acted in.
select concat(a.first_name, ' ', a.last_name) as name , title
from actor a
inner join 
film_actor on a.actor_id = film_actor.actor_id
inner join
film on film_actor.film_id =film.film_id;
select title from film where film_id in (select distinct film_id from inventory);




