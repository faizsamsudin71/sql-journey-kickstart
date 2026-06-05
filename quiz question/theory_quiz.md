# SQL Theory Quiz Questions

This document contains the 10 theory quiz questions extracted from the training portal's Assessment section.

---

### Question 1: Foreign Key Purpose
In a relational database, what is the primary purpose of a Foreign Key?
- A) To uniquely identify each row in a table.
- **B) To establish a link between two tables and enforce referential integrity.** (Correct)
- C) To speed up data retrieval times.
- D) To allow multiple columns to store NULL values.

**Explanation:** Foreign keys link rows in one table to primary keys in another table, maintaining consistent structural linkages between entities.

---

### Question 2: Aggregate Filtering
Which SQL clause is used to filter rows AFTER they have been grouped by an aggregate function?
- A) WHERE
- **B) HAVING** (Correct)
- C) GROUP BY
- D) ORDER BY

**Explanation:** HAVING filters groups created by GROUP BY, while WHERE filters individual rows before grouping operations occur.

---

### Question 3: NULL Comparison
Consider the query: `SELECT * FROM WELL WHERE rig_id = NULL;`. What is wrong with this query?
- A) You cannot select all columns using `*`.
- B) The table name `WELL` must be lowercase.
- **C) To check for NULL values, SQL requires 'IS NULL' instead of '= NULL'.** (Correct)
- D) `rig_id` cannot be checked for NULL.

**Explanation:** In SQL, comparing anything with NULL using `=` returns UNKNOWN. You must use `IS NULL` or `IS NOT NULL` to compare properly.

---

### Question 4: Left Join Behavior
Which JOIN type returns all records from the left table, and the matched records from the right table, filling in NULLs on the right where there is no match?
- A) INNER JOIN
- B) RIGHT JOIN
- C) FULL OUTER JOIN
- **D) LEFT JOIN** (Correct)

**Explanation:** A LEFT JOIN retains all records from the left table and inserts NULLs for columns from the right table if no match is found.

---

### Question 5: Row Counting
What does the query `SELECT COUNT(*) FROM REPORT_JOURNAL;` do?
- A) Counts the number of tables in the database.
- B) Counts the number of columns in the `REPORT_JOURNAL` table.
- **C) Counts the total number of rows (reports) in the `REPORT_JOURNAL` table.** (Correct)
- D) Returns the first row of the `REPORT_JOURNAL` table.

**Explanation:** `COUNT(*)` counts all rows in the target table, regardless of columns contents or NULL presence.

---

### Question 6: Eliminating Duplicates
If you want to eliminate duplicate rows from a query's output, which keyword should you use?
- A) UNIQUE
- **B) DISTINCT** (Correct)
- C) GROUP BY
- D) ROW_NUMBER

**Explanation:** DISTINCT filters the results to ensure that only unique value sets are printed in the final output.

---

### Question 7: Common Table Expressions (CTEs)
What is a key characteristic of Common Table Expressions (CTEs)?
- A) They are permanently stored in the database.
- **B) They are written using the `WITH` keyword and exist only for the duration of the query.** (Correct)
- C) They run slower than subqueries in all database engines.
- D) They do not support joins.

**Explanation:** CTEs are declared using the `WITH` clause. They are temporary expression sets that reside entirely within query compilation memory.

---

### Question 8: Window Functions
Which window function would you use to assign a sequential number to each row within a partition, starting at 1 for each partition?
- A) RANK()
- B) DENSE_RANK()
- **C) ROW_NUMBER()** (Correct)
- D) SUM()

**Explanation:** `ROW_NUMBER()` assigns a strictly sequential row index starting at 1 for each partition group defined in the `OVER` clause.

---

### Question 9: Orphan Records
What is an 'orphan record' in database terms?
- A) A record in a parent table that has no child records.
- **B) A record in a child table whose foreign key points to a non-existent parent primary key.** (Correct)
- C) A record that has been deleted.
- D) A record with NULL values in all its columns.

**Explanation:** An orphan record violates referential integrity. Its foreign key contains a value referencing a parent row that does not exist.

---

### Question 10: Handling NULLs
Which SQL function can be used to replace a NULL value with a default value?
- A) COALESCE()
- B) IFNULL()
- **C) Either A or B** (Correct)
- D) Neither A nor B

**Explanation:** `COALESCE()` is standard ANSI SQL and returns the first non-NULL argument, while `IFNULL()` is a popular database function that does the same.
