# show variables like '%profiling%';
# set profiling = 1;
# set profiling_history_size = 15;
# show profiles;
# show profiles;
/*
SELECT DISTINCT CONCAT(e.first_name, ' ', e.last_name) Name 
FROM employees e, salaries s
WHERE e.emp_no = s.emp_no AND s.salary > 100000;
*/
# show profiles;
show profile cpu for query 21
/*
SELECT DISTINCT CONCAT(e.first_name, ' ', e.last_name) Name 
FROM employees e
WHERE e.emp_no IN (
SELECT DISTINCT s.emp_no 
FROM salaries s 
WHERE s.salary > 100000)
*/

