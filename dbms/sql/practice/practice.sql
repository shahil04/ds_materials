show databases;

use mavenmovies;

select title , rental_rate from film where rental_rate > 4;
select first_name , last_name , email , address_id from customer where address_id = 300;

SELECT * FROM film WHERE title REGEXP '^[A-Z][a-z]*R$';
SELECT * FROM film WHERE title REGEXP '^[A-Z][a-z]*( [A-Z][a-z]*)*R$';

-- not use with like
SELECT * FROM film WHERE title LIKE '[A-Z]*a%';

-- ^: Asserts the position at the start of the string.
-- [A-Z]: Matches any uppercase letter from A to Z at the beginning of the string.
-- [a-z]*: Matches zero or more lowercase letters.
-- ( [A-Z][a-z]*)*: Matches zero or more occurrences of a space followed by an uppercase letter and zero or more lowercase letters.
-- R: Matches the character 'R' at the end.
-- $: Asserts the position at the end of the string.