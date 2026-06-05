# Getting Started: SQL Mastery Course

Welcome to the SQL Mastery training! This guide will help you set up your environment in under 2 minutes.

---

## 🚀 Step 1: Start the Interactive Training Portal

The training portal is an interactive companion containing the database explorer, exercise slides, solution panels, and the final quiz.

1. **Launch the Local Server:**
   * **Windows:** Double-click **[start_portal.bat](start_portal.bat)** in this directory.
   * **macOS/Linux:** Open a terminal in this directory and run:
     ```bash
     cd portal && python3 -m http.server 8000
     ```
2. **Open the Portal:**
   * Navigate to **[http://localhost:8000/index.html](http://localhost:8000/index.html)** in your web browser.
   * Access the **Database Explorer** tab on the sidebar to inspect tables side-by-side with your exercises.

---

## 💾 Step 2: Connect Your SQL Client

To write and run your queries during the hands-on sessions, connect a local database client:

1. Open **DBeaver** or **DB Browser for SQLite**.
2. Create a new database connection and select **SQLite** as the database type.
3. Browse and select the **[drilling_course.db](database/drilling_course.db)** file located in the **database** subdirectory of this workspace.
4. Open a new SQL Editor/Console to start querying.

---

## 📚 Course Materials Reference

* **Interactive Portal ([localhost:8000](http://localhost:8000/index.html)):** Your primary companion during the training day for exploring tables, reading exercise objectives, revealing solution SQL, and taking the assessment.
* **Comprehensive Workbook ([sql_workbook.md](course_materials/sql_workbook.md)):** Contains full theoretical notes, schema explanations, normalization rules, and printable example listings.
