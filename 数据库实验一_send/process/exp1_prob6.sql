# 查询至少在2个部门工作过的员工人数
USE employee;
SELECT COUNT(*) cnt
FROM 
(
	SELECT emp_no
	FROM dept_emp
	GROUP BY dept_emp.emp_no HAVING COUNT(*) >= 2
) res;
