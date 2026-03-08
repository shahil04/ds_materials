-- RENAME TABLE old_table_name TO new_table_name;
RENAME TABLE `cleaned_data (3)` TO `clean`;
SHOW VARIABLES LIKE 'secure_file_priv';
-- secure_file_priv, C:\ProgramData\MySQL\MySQL Server 9.4\Uploads\

truncate clean;
LOAD DATA INFILE 'C:\\ProgramData\\MySQL\\MySQL Server 9.4\\Uploads\\Cleaned.csv'
INTO TABLE clean
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES;
