# 查询没有在“Production”部门工作过且first_name 是“Ge”开头的的员工信息，
# 显示其 emp_no, birth_date, first_name, last_name, gender, hire_date；
USE employee;
SELECT DISTINCT employees.emp_no, birth_date, first_name, last_name, gender, hire_date
FROM employees, departments, dept_emp
WHERE
	employees.emp_no = dept_emp.emp_no AND
    dept_emp.dept_no = departments.dept_no AND
    departments.dept_name <> 'Production' AND
    first_name LIKE 'Ge%';