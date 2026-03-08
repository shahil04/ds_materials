use mavenmovies;
show tables;

select * from actor;
select * from payment;

select amount -1 from payment;

update payment 
set amount = amount -1
where payment_id =true;

select (amount *10)/100 from payment;

-- relational operators 
select *  from payment
where amount > 2;

select * from payment;

select * from payment 
where amount <= 1;

select * from payment 
where amount >= 1;


-- and
select *  from actor_award;

select  * from actor_award
where last_name ="BERRY";


select * from actor_award
where awards ='Emmy' or last_name="berry";

select * from actor_award
where awards !='Emmy';

-- between 
select * from  actor_award
where actor_award_id between 1 and 8 ;

-- in 
select * from actor_award
where actor_award_id in (2,3,5,979895658);


-- wild card	
select * from actor_Award
where first_name like "_i%";

-- limit 
select * from actor_Award
where first_name like "_i%"
limit 5;

-- order by 
select * from actor_Award
order by awards desc;

-- allies 
select  first_name as n  from actor_award;

-- distinct
select distinct first_name from actor_Award;

-- is null 
select * from actor_award
where actor_id is null;

-- not null
select * from actor_award
where actor_id is not null;

select	* from actor_award
where  first_name like "s%n";
