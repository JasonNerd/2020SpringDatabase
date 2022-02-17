# ① 查询emp_no是“10029”的员工信息，显示其 emp_no, birth_date, first_name, last_name, gender, hire_date, title；
USE employee;
SELECT employees.emp_no, birth_date, first_name, last_name, gender, hire_date, title
FROM employees, titles
WHERE employees.emp_no = titles.emp_no AND
	  employees.emp_no = '10029';