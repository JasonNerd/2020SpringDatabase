# 查询在“d003”部门工作过的且工资最高的员工编号及其最高工资；
USE employee;
SELECT dept_emp.emp_no, MAX(salaries.salary) as PerMax
FROM dept_emp, salaries
WHERE dept_emp.emp_no = salaries.emp_no AND
	  dept_emp.dept_no = 'd003'
GROUP BY dept_emp.emp_no
ORDER BY PerMax DESC
LIMIT 1