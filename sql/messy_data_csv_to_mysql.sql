-- Database Creation
CREATE DATABASE retail_db;
USE retail_db;

-- creating table in the retail_db database
CREATE TABLE retail_sales (
    transaction_id VARCHAR(20),
    customer_id VARCHAR(20),
    category VARCHAR(50),
    item VARCHAR(50) NULL,
    price_per_unit DECIMAL(10,2) NULL,
    quantity INT NULL,
    total_spent DECIMAL(10,2) NULL,
    payment_method VARCHAR(30),
    location VARCHAR(20),
    transaction_date DATE,
    discount_applied VARCHAR(20) NULL
);


-- loading csv file into table (null values handling)
LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/retail_store_sales.csv'
INTO TABLE retail_sales
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(
 transaction_id,
 customer_id,
 category,
 @item,
 @price_per_unit,
 @quantity,
 @total_spent,
 payment_method,
 location,
 transaction_date,
 @discount_applied
)
SET
 item = NULLIF(@item, ''),
 price_per_unit = NULLIF(@price_per_unit, ''),
 quantity = NULLIF(@quantity, ''),
 total_spent = NULLIF(@total_spent, ''),
 discount_applied = NULLIF(@discount_applied, '');


-- Data Exploration
-- checking total rows
SELECT COUNT(*) FROM retail_sales;

-- display 10 rows from the data 
SELECT * 
FROM retail_sales
limit 10;


-- Check NULL count for each column in the table
SELECT
    SUM(transaction_id IS NULL) AS transaction_id_nulls,
    SUM(customer_id IS NULL) AS customer_id_nulls,
    SUM(category IS NULL) AS category_nulls,
    SUM(item IS NULL) AS item_nulls,
    SUM(price_per_unit IS NULL) AS price_per_unit_nulls,
    SUM(quantity IS NULL) AS quantity_nulls,
    SUM(total_spent IS NULL) AS total_spent_nulls,
    SUM(payment_method IS NULL) AS payment_method_nulls,
    SUM(location IS NULL) AS location_nulls,
    SUM(transaction_date IS NULL) AS transaction_date_nulls,
    SUM(discount_applied IS NULL) AS discount_applied_nulls
FROM retail_sales;


SELECT DISTINCT discount_applied
FROM retail_sales;




