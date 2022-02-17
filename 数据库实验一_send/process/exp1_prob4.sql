# 查询 first_name 相同且人数超过3人的员工信息，显示其 emp_no, birth_date, 
# first_name, last_name, gender, hire_date，要求按first_name升序显示
USE employee;
SELECT TA.emp_no, TA.first_name, TA.last_name, TA.gender, TA.hire_date
FROM employees TA, employees TB
WHERE TA.emp_no <> TB.emp_no AND TA.first_name = TB.first_name
GROUP BY TA.first_name HAVING count(*)>=3
ORDER BY TA.first_name;