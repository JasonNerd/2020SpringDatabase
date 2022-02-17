# CREATE DATABASE employee
/*
USE employee;
CREATE TABLE departments ( 
	dept_no CHAR(4) NOT NULL, 
	dept_name VARCHAR(40) NOT NULL, 
	PRIMARY KEY (dept_no), 
	UNIQUE KEY (dept_name)
);
*/
/*
DROP TABLE `employee`.`salaries`;
CREATE TABLE `employee`.`salaries` (
  `emp_no` INT NOT NULL,
  `salary` INT NULL,
  `from_date` DATE NULL,
  `to_date` DATE NULL
  );
*/
/*
DROP TABLE `employee`.`emploees`;
CREATE TABLE `employee`.`emploees`(
	`emp_no` INT NOT NULL,
    `birth_date` DATE NULL,
    `first_name` VARCHAR(20) NULL,
    `last_name` VARCHAR(20) NULL,
    `gender` ENUM('M', 'F') NULL,
    `hire_date` DATE NULL,
    PRIMARY KEY (`emp_no`)
);
*/
/*
CREATE TABLE `employee`.`titles`(
	`emp_no` INT NOT NULL,
	`title` VARCHAR(40) NULL,
    `from_date` DATE NULL,
    `to_date` DATE NULL
);
*/
/*
CREATE TABLE `employee`.`dept_emp`(
	`emp_no` INT NOT NULL,
	`title` VARCHAR(40) NULL,
    `from_date` DATE NULL,
    `to_date` DATE NULL
);
*/

CREATE TABLE `employee`.`dept_manager`(
	`emp_no` INT NOT NULL,
	`dept_no` CHAR(4) NULL,
    `from_date` DATE NULL,
    `to_date` DATE NULL
);