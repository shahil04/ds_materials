-- ----------------------------------------------------------------------------
-- MySQL Workbench Migration
-- Migrated Schemata: class_11
-- Source Schemata: class_11_1
-- Created: Thu Mar 13 12:40:47 2025
-- Workbench Version: 8.0.38
-- ----------------------------------------------------------------------------

SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------------------------------------------------------
-- Schema class_11
-- ----------------------------------------------------------------------------
DROP SCHEMA IF EXISTS `class_11` ;
CREATE SCHEMA IF NOT EXISTS `class_11` ;

-- ----------------------------------------------------------------------------
-- Table class_11.authors
-- ----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS `class_11`.`authors` (
  `Author_ID` INT NULL DEFAULT NULL,
  `Author_Name` VARCHAR(100) NULL DEFAULT NULL)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;

-- ----------------------------------------------------------------------------
-- Table class_11.books
-- ----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS `class_11`.`books` (
  `Book_ID` INT NULL DEFAULT NULL,
  `Title` VARCHAR(100) NULL DEFAULT NULL,
  `AuthorID` INT NULL DEFAULT NULL,
  `Price` DECIMAL(10,2) NULL DEFAULT NULL,
  `Publication_Year` INT NULL DEFAULT NULL,
  `Quantity_In_Stock` INT NULL DEFAULT NULL)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;

-- ----------------------------------------------------------------------------
-- Table class_11.catagory
-- ----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS `class_11`.`catagory` (
  `new_id` INT NULL DEFAULT NULL,
  `new_cat` VARCHAR(50) NULL DEFAULT NULL,
  INDEX `my_index` (`new_cat` ASC) VISIBLE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;

-- ----------------------------------------------------------------------------
-- Table class_11.course
-- ----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS `class_11`.`course` (
  `c_id` INT NOT NULL,
  `course_name` VARCHAR(100) NOT NULL,
  `fee` FLOAT NOT NULL,
  PRIMARY KEY (`c_id`),
  UNIQUE INDEX `course_name` (`course_name` ASC) VISIBLE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;

-- ----------------------------------------------------------------------------
-- Table class_11.customers
-- ----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS `class_11`.`customers` (
  `Customer_ID` INT NULL DEFAULT NULL,
  `Customer_Name` VARCHAR(100) NULL DEFAULT NULL,
  `Address` VARCHAR(250) NULL DEFAULT NULL,
  `Contact_Info` VARCHAR(150) NULL DEFAULT NULL)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;

-- ----------------------------------------------------------------------------
-- Table class_11.employee
-- ----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS `class_11`.`employee` (
  `id` INT NOT NULL,
  `workdate` DATE NOT NULL,
  PRIMARY KEY (`id`, `workdate`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;

-- ----------------------------------------------------------------------------
-- Table class_11.employee2
-- ----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS `class_11`.`employee2` (
  `id` INT NOT NULL,
  `workdate` DATE NOT NULL,
  PRIMARY KEY (`id`, `workdate`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;

-- ----------------------------------------------------------------------------
-- Table class_11.orders
-- ----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS `class_11`.`orders` (
  `Order_ID` INT NULL DEFAULT NULL,
  `Customer_ID` INT NULL DEFAULT NULL,
  `Book_ID` INT NULL DEFAULT NULL,
  `Quantity` INT NULL DEFAULT NULL,
  `Total_Price` DECIMAL(10,2) NULL DEFAULT NULL)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;

-- ----------------------------------------------------------------------------
-- Table class_11.students
-- ----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS `class_11`.`students` (
  `std_id` INT NOT NULL,
  `name` VARCHAR(100) NOT NULL,
  `phone_number` INT NULL DEFAULT NULL,
  `age` INT NULL DEFAULT NULL,
  `course_id` INT NULL DEFAULT NULL,
  PRIMARY KEY (`std_id`),
  UNIQUE INDEX `phone_number` (`phone_number` ASC) VISIBLE,
  INDEX `course_id` (`course_id` ASC) VISIBLE,
  CONSTRAINT `students_ibfk_1`
    FOREIGN KEY (`course_id`)
    REFERENCES `class_11`.`course` (`c_id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;

-- ----------------------------------------------------------------------------
-- Table class_11.your_table_name
-- ----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS `class_11`.`your_table_name` (
  `new_id` INT NULL DEFAULT NULL,
  `new_cat` VARCHAR(50) NULL DEFAULT NULL)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;

-- ----------------------------------------------------------------------------
-- View class_11.window_func
-- ----------------------------------------------------------------------------
USE `class_11`;
CREATE  OR REPLACE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `class_11_1`.`window_func` AS select `class_11_1`.`your_table_name`.`new_cat` AS `new_cat`,`class_11_1`.`your_table_name`.`new_id` AS `new_id`,sum(`class_11_1`.`your_table_name`.`new_id`) OVER (PARTITION BY `class_11_1`.`your_table_name`.`new_cat` )  AS `category_total`,sum(`class_11_1`.`your_table_name`.`new_id`) OVER ()  AS `total`,avg(`class_11_1`.`your_table_name`.`new_id`) OVER (PARTITION BY `class_11_1`.`your_table_name`.`new_cat` )  AS `cat_avg`,avg(`class_11_1`.`your_table_name`.`new_id`) OVER ()  AS `total_Avg`,count(`class_11_1`.`your_table_name`.`new_id`) OVER (PARTITION BY `class_11_1`.`your_table_name`.`new_cat` )  AS `cat_wise_count`,count(`class_11_1`.`your_table_name`.`new_id`) OVER ()  AS `total_count` from `class_11_1`.`your_table_name`;
SET FOREIGN_KEY_CHECKS = 1;
