USE uber_demo;
INSERT INTO users (name, phone, role) VALUES
('Alice Rider','+911234567890','rider'),
('Bob Rider','+919876543210','rider');
INSERT INTO riders (user_id, default_payment_method) VALUES (1,'card'),(2,'cash');
INSERT INTO users (name, phone, role) VALUES
('Driver Dan','+919440000111','driver'),
('Driver Priya','+919440000222','driver'),
('Driver Kumar','+919440000333','driver');
INSERT INTO drivers (user_id, vehicle, lat, lon, available) VALUES
(3,'Swift',28.644800,77.216721,TRUE),
(4,'Ertiga',28.650000,77.230000,TRUE),
(5,'Dzire',28.630000,77.210000,TRUE);
