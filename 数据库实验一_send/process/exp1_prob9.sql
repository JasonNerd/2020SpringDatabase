SELECT dept_emp.dept_no, SUM(salaries.salary) AllSalary
FROM dept_emp, salaries
WHERE dept_emp.emp_no = salaries.emp_no
	  AND YEAR(salaries.to_date) = '9999'
	  GROUP BY dept_emp.dept_no
