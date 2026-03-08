use class_11_1;

CREATE TABLE employee (
    id INT NOT NULL,
    workdate DATE NOT NULL,
    PRIMARY KEY (id, workdate)
);
---
INSERT INTO employee (id, workdate)
VALUES
    (1, '2024-10-21'),
    (1, '2024-10-23'),  -- Break in consecutive days
    (2, '2024-10-21'),
    (2, '2024-10-22'),  -- 2 consecutive days
    (3, '2024-10-19'),
    (3, '2024-10-20'),  -- 2 consecutive days
    (4, '2024-10-21'),
    (4, '2024-10-22'),
    (4, '2024-10-23'),  -- 3 consecutive days
    (5, '2024-10-25'),
    (6, '2024-10-27'),
    (6, '2024-10-28'),
    (6, '2024-10-30'),  -- Break in consecutive days
    (7, '2024-10-21'),
    (7, '2024-10-22'),
    (8, '2024-10-24'),
    (8, '2024-10-26'),  -- Break in consecutive days
    (9, '2024-10-23'),
    (9, '2024-10-24'),
    (9, '2024-10-25'),  -- 3 consecutive days
    (10, '2024-10-26'),
    (10, '2024-10-28'), -- Break in consecutive days
    (11, '2024-10-27'),
    (11, '2024-10-29'), -- Break in consecutive days
    (12, '2024-10-24'),
    (12, '2024-10-25'), -- 2 consecutive days
    (13, '2024-10-21'),
    (13, '2024-10-22'),
    (13, '2024-10-23'), -- 3 consecutive days
    (14, '2024-10-22'), -- Single day
    (15, '2024-10-23'),
    (15, '2024-10-25'); -- Break in consecutive days

-- 1st way 
SELECT DISTINCT e1.id
FROM employee e1
JOIN employee e2 ON e1.id = e2.id AND e1.workdate = DATE_ADD(e2.workdate, INTERVAL 1 DAY)
JOIN employee e3 ON e1.id = e3.id AND e1.workdate = DATE_ADD(e3.workdate, INTERVAL 2 DAY)
ORDER BY e1.id;

-- 2nd way
WITH consecutive_days AS (
    SELECT 
        id, 
        workdate,
        LAG(workdate, 1) OVER (PARTITION BY id ORDER BY workdate) AS prev_day,
        LEAD(workdate, 1) OVER (PARTITION BY id ORDER BY workdate) AS next_day
    FROM employee
)
SELECT DISTINCT id
FROM consecutive_days
WHERE 
    DATE_ADD(prev_day, INTERVAL 1 DAY) = workdate
    AND DATE_ADD(workdate, INTERVAL 1 DAY) = next_day;


