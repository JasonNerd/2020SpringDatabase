# 查询入职时间在1990年后且在“Finance”部门工作过的男员工姓名；
USE employee;
SELECT CONCAT(first_name, ' ', last_name) PNAME
FROM employees, departments, dept_emp
WHERE
	employees.emp_no = dept_emp.emp_no AND
    departments.dept_no = dept_emp.dept_no AND
    departments.dept_name = 'Finance' AND
    employees.gender = 'M' AND
    YEAR(employees.hire_date) > '1990';