# 在departments表中修改步骤11新增的记录
UPDATE departments
SET dept_name = 'Party Affairs'
WHERE dept_no = 'd00b';
SELECT * FROM employee.departments;