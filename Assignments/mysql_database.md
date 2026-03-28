# MySQL Database

## CREATE TABLE employees
```sql
CREATE TABLE employees (
    emp_id INT PRIMARY KEY,
    emp_name VARCHAR(100),
    emp_email VARCHAR(150)
);
```

## CREATE TABLE departments
```sql
CREATE TABLE departments (
    emp_id INT,
    dept_name VARCHAR(100)
);
```

## INSERT INTO employees VALUES
```sql
INSERT INTO employees VALUES
(101, 'Pardhu', 'pardhu@gmail.com'),
(102, 'ankit', 'ankit@gmail.com'),
(103, 'hemanjali', 'hemanjali@gmail.com');

INSERT INTO employees VALUES
(104, 'Pardhu', 'pardhu@gmail.com');
```

## INSERT INTO departments VALUES
```sql
INSERT INTO departments VALUES
(101, 'IT'),
(102, 'HR');
```

## SELECT Queries

### INNER JOIN Query
```sql
SELECT u.emp_id, u.emp_name, d.dept_name
FROM employees u
INNER JOIN departments d
ON u.emp_id = d.emp_id;
```

### LEFT JOIN Query
```sql
SELECT u.emp_id, u.emp_name, d.dept_name
FROM employees u
LEFT JOIN departments d
ON u.emp_id = d.emp_id;
```

### GROUP BY Query
```sql
select emp_name, min(emp_id) from employees group by emp_name;
```

## Query Output

| emp_id | emp_name | dept_name |
|--------|----------|-----------|
| 101 | Pardhu | IT |
| 102 | ankit | HR |

### LEFT JOIN Output

| emp_id | emp_name | dept_name |
|--------|----------|-----------|
| 101 | Pardhu | IT |
| 102 | ankit | HR |
| 103 | hemanjali | NULL |
| 104 | Pardhu | NULL |

### GROUP BY Output

| emp_name | min(emp_id) |
|----------|------------|
| ankit | 102 |
| hemanjali | 103 |
| Pardhu | 101 |