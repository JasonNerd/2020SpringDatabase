# 查询当前部门员工平均工资在70000元到80000元
#（包含70000，低于80000）的部门编号，部门名称和员工平均工资；
USE employee;
SELECT dept_emp.dept_no, departments.dept_name, AVG(salaries.salary) as aver
FROM dept_emp, departments, salaries
WHERE dept_emp.emp_no = salaries.emp_no
	AND departments.dept_no = dept_emp.dept_no
    AND YEAR(dept_emp.to_date) = '9999'
    AND salaries.salary >= 70000
    AND salaries.salary < 80000
    GROUP BY dept_emp.dept_no