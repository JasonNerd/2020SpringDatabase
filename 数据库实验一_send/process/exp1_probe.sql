# 新建视图，查询所有在1990年后入职过“Finance”部门的男员工信息，
# 包括：emp_no, birth_date, first_name, last_name, hire_date, from_date, to_date
/*
SELECT employees.emp_no, birth_date, first_name, last_name, hire_date, from_date, to_date
FROM employees, departments, dept_emp
WHERE employees.emp_no = dept_emp.emp_no
	AND dept_emp.dept_no = departments.dept_no
    AND departments.dept_name = 'Finance'
    AND employees.gender = 'M'
    AND YEAR(dept_emp.from_date) >= '1990';
*/

CREATE VIEW MFEMP AS(
	SELECT *
    FROM employees
    WHERE employees.gender = 'M'
);
SELECT MFEMP.emp_no, birth_date, first_name, last_name, hire_date, from_date, to_date
FROM MFEMP, departments, dept_emp
WHERE MFEMP.emp_no = dept_emp.emp_no
	AND dept_emp.dept_no = departments.dept_no
    AND departments.dept_name = 'Finance'
	AND YEAR(dept_emp.from_date) >= '1990';
