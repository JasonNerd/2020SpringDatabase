# 查询“d002”部门的当前领导姓名
USE employee;
SELECT CONCAT(employees.first_name, ' ', employees.last_name) Manager
FROM employees, dept_manager
WHERE employees.emp_no = dept_manager.emp_no 
	  AND dept_manager.dept_no = 'd002' 
      AND YEAR(dept_manager.to_date) = '9999'
      