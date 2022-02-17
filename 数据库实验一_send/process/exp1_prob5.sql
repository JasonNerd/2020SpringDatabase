# 查询至少在“Production”和“Quality Management”
# 两个部门都工作过的员工编号
USE employee;
SELECT employees.emp_no
FROM employees, dept_emp, departments
WHERE employees.emp_no = dept_emp.emp_no AND
	  dept_emp.dept_no = departments.dept_no AND
	  departments.dept_name = 'Production'
      AND employees.emp_no IN(
SELECT employees.emp_no
FROM employees, dept_emp, departments
WHERE employees.emp_no = dept_emp.emp_no AND
	  dept_emp.dept_no = departments.dept_no AND
	  departments.dept_name = 'Quality Management'
)