use uber;
-- data type change 
desc customers;

alter table customers
modify column customer_id varchar(100) primary key; 
desc  bookings;
alter table bookings
modify column customer_id varchar(100) ; 

ALTER TABLE bookings
ADD CONSTRAINT customer_id
FOREIGN KEY (customer_id)
REFERENCES customers(customer_id);

-- =========================
ALTER TABLE customers
ADD CONSTRAINT customer_id
FOREIGN KEY (customer_id)	
REFERENCES bookings(customer_id);

select * FROM bookings
WHERE customer_id NOT IN (SELECT customer_id FROM customers);

delete FROM bookings
WHERE customer_id NOT IN (SELECT customer_id FROM customers);

ALTER TABLE child_table_name
ADD CONSTRAINT fk_name
FOREIGN KEY (child_column_name)
REFERENCES parent_table_name(parent_column_name)
;

desc feedback;
