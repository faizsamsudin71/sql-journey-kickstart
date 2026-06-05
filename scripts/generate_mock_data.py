import sqlite3
import random
from datetime import datetime, timedelta
import os

# Define absolute paths relative to the script location
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)
db_path = os.path.join(project_root, 'database', 'drilling_course.db')
html_path = os.path.join(project_root, 'portal', 'index.html')
md_path = os.path.join(project_root, 'course_materials', 'sql_workbook.md')

def create_database():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Drop tables if they exist for clean generation
    tables = [
        "COMPLETION_PHASE_DETAILS", "DRILLING_PHASE_DETAILS", 
        "REPORT_JOURNAL", "WELL_PHASE", "PHASE", "WELL", "RIG"
    ]
    for t in tables:
        cursor.execute(f"DROP TABLE IF EXISTS {t}")

    # Note: Using INTEGER PRIMARY KEY instead of UUIDs to make it easier for 
    # beginners to write queries during the training.
    
    cursor.execute('''
    CREATE TABLE RIG (
        rig_id INTEGER PRIMARY KEY AUTOINCREMENT,
        rig_name TEXT NOT NULL
    )''')

    cursor.execute('''
    CREATE TABLE WELL (
        well_id INTEGER PRIMARY KEY AUTOINCREMENT,
        rig_id INTEGER,
        well_name TEXT NOT NULL,
        FOREIGN KEY (rig_id) REFERENCES RIG(rig_id)
    )''')

    cursor.execute('''
    CREATE TABLE PHASE (
        phase_id INTEGER PRIMARY KEY AUTOINCREMENT,
        phase_name TEXT NOT NULL
    )''')

    cursor.execute('''
    CREATE TABLE WELL_PHASE (
        well_phase_id INTEGER PRIMARY KEY AUTOINCREMENT,
        well_id INTEGER,
        phase_id INTEGER,
        FOREIGN KEY (well_id) REFERENCES WELL(well_id),
        FOREIGN KEY (phase_id) REFERENCES PHASE(phase_id)
    )''')

    cursor.execute('''
    CREATE TABLE REPORT_JOURNAL (
        report_journal_id INTEGER PRIMARY KEY AUTOINCREMENT,
        well_phase_id INTEGER,
        report_datetime DATETIME,
        report_type TEXT,
        FOREIGN KEY (well_phase_id) REFERENCES WELL_PHASE(well_phase_id)
    )''')

    cursor.execute('''
    CREATE TABLE DRILLING_PHASE_DETAILS (
        drilling_phase_id INTEGER PRIMARY KEY AUTOINCREMENT,
        well_phase_id INTEGER,
        report_journal_id INTEGER,
        plan_cost REAL,
        actual_cost REAL,
        FOREIGN KEY (well_phase_id) REFERENCES WELL_PHASE(well_phase_id),
        FOREIGN KEY (report_journal_id) REFERENCES REPORT_JOURNAL(report_journal_id)
    )''')

    cursor.execute('''
    CREATE TABLE COMPLETION_PHASE_DETAILS (
        completion_phase_id INTEGER PRIMARY KEY AUTOINCREMENT,
        well_phase_id INTEGER,
        report_journal_id INTEGER,
        plan_cost REAL,
        actual_cost REAL,
        FOREIGN KEY (well_phase_id) REFERENCES WELL_PHASE(well_phase_id),
        FOREIGN KEY (report_journal_id) REFERENCES REPORT_JOURNAL(report_journal_id)
    )''')

    return conn, cursor

def populate_data(conn, cursor):
    random.seed(42)  # For deterministic generation

    # 1. RIGS
    rigs = ["Ocean Valor", "Deepwater Horizon", "Deepsea Aberdeen", "Valaris DS-12", "Transocean Barents"]
    for rig in rigs:
        cursor.execute("INSERT INTO RIG (rig_name) VALUES (?)", (rig,))
    
    # 2. PHASES
    phases = ["Exploration", "Development", "Intervention", "Workover", "Plug and abandonment"]
    for phase in phases:
        cursor.execute("INSERT INTO PHASE (phase_name) VALUES (?)", (phase,))
        
    # 3. WELLS
    # Ghost-1 is added so it exists in WELL but has no active phases or reports for Exercise 2.1
    wells = ["Alpha-1", "Alpha-2", "Bravo-1", "Charlie-1", "Delta-X", "Echo-99", "Ghost-1"]
    for well in wells:
        rig_id = random.randint(1, len(rigs))
        cursor.execute("INSERT INTO WELL (rig_id, well_name) VALUES (?, ?)", (rig_id, well))
        
    # 4. WELL_PHASES
    for well_id in range(1, len(wells) + 1):
        if wells[well_id - 1] == "Ghost-1":
            continue
        # Each well goes through 2 to 4 phases
        num_phases = random.randint(2, 4)
        selected_phases = random.sample(range(1, len(phases) + 1), num_phases)
        selected_phases.sort() # Logical progression
        
        for phase_id in selected_phases:
            cursor.execute("INSERT INTO WELL_PHASE (well_id, phase_id) VALUES (?, ?)", (well_id, phase_id))

    # 5. REPORTS & DETAILS
    start_date = datetime(2025, 1, 1)
    
    # Get all well phases
    cursor.execute("SELECT well_phase_id, phase_id FROM WELL_PHASE")
    well_phases = cursor.fetchall()
    
    report_id = 1
    for wp_id, phase_id in well_phases:
        if phase_id == 1:
            report_types = ["NOOP", "FWR"]
        elif phase_id == 2:
            report_types = ["NOOC", "FWC"]
        elif phase_id == 3:
            report_types = ["Int Report 1", "Int Report 2"]
        elif phase_id == 4:
            report_types = ["Wov Report 1", "Wov Report 2"]
        elif phase_id == 5:
            report_types = ["P&A Report 1", "P&A Report 2"]
            
        current_date = start_date + timedelta(days=random.randint(0, 100))
        
        for report_type in report_types:
            # Insert Report Journal
            cursor.execute("INSERT INTO REPORT_JOURNAL (well_phase_id, report_datetime, report_type) VALUES (?, ?, ?)", 
                           (wp_id, current_date.strftime("%Y-%m-%d %H:%M:%S"), report_type))
            
            # Insert Details based on phase type (Assume phase 1-3 is drilling, 4 is completion)
            plan_cost = round(random.uniform(50000, 150000), 2)
            actual_cost = round(plan_cost * random.uniform(0.8, 1.3), 2) # Actuals fluctuate around plan
            
            if phase_id == 1: # Drilling phases
                cursor.execute("INSERT INTO DRILLING_PHASE_DETAILS (well_phase_id, report_journal_id, plan_cost, actual_cost) VALUES (?, ?, ?, ?)",
                               (wp_id, report_id, plan_cost, actual_cost))
            elif phase_id == 2: # Completion
                cursor.execute("INSERT INTO COMPLETION_PHASE_DETAILS (well_phase_id, report_journal_id, plan_cost, actual_cost) VALUES (?, ?, ?, ?)",
                               (wp_id, report_id, plan_cost, actual_cost))
            
            report_id += 1
            current_date += timedelta(days=1)

    # --- INJECT INTENTIONAL DIRTY DATA FOR SESSION 4 (DATA CLEANING) ---
    print("Injecting intentional dirty data for Session 4...")
    
    # Dirty Data 1: Orphan Records (Details with non-existent report journals or well phases)
    cursor.execute("INSERT INTO DRILLING_PHASE_DETAILS (well_phase_id, report_journal_id, plan_cost, actual_cost) VALUES (999, 9999, 100000.0, 120000.0)")
    cursor.execute("INSERT INTO COMPLETION_PHASE_DETAILS (well_phase_id, report_journal_id, plan_cost, actual_cost) VALUES (888, 8888, 50000.0, 55000.0)")
    
    # Dirty Data 2: Duplicates in REPORT_JOURNAL
    cursor.execute("SELECT well_phase_id, report_datetime, report_type FROM REPORT_JOURNAL LIMIT 3")
    duplicates = cursor.fetchall()
    for dup in duplicates:
        # Insert exact same records again to create true duplicates
        cursor.execute("INSERT INTO REPORT_JOURNAL (well_phase_id, report_datetime, report_type) VALUES (?, ?, ?)", dup)

    # Dirty Data 3: Null Values
    # Some actual costs are NULL (e.g. costs not yet finalized)
    cursor.execute("UPDATE DRILLING_PHASE_DETAILS SET actual_cost = NULL WHERE drilling_phase_id IN (3, 5)")
    
    conn.commit()

def sync_examples(conn):
    import re
    cursor = conn.cursor()
    
    # 1. Define queries matching course materials
    queries = {
        "S1_E1": {
            "sql": """SELECT well_name, rig_id
FROM WELL
WHERE well_name LIKE 'Alpha%'
ORDER BY well_name ASC;"""
        },
        "S1_E2": {
            "sql": """SELECT rj.report_journal_id, w.well_name, rj.report_type
FROM REPORT_JOURNAL rj
JOIN WELL_PHASE wp ON rj.well_phase_id = wp.well_phase_id
JOIN WELL w ON wp.well_id = w.well_id
WHERE rj.report_type = 'NOOP';""",
            "limit": 5
        },
        "S1_E3": {
            "sql": """SELECT well_phase_id, SUM(actual_cost) AS total_actual_cost
FROM DRILLING_PHASE_DETAILS
GROUP BY well_phase_id
HAVING SUM(actual_cost) > 200000;"""
        },
        "S2_E1A": {
            "sql": """SELECT drilling_phase_id, well_phase_id, actual_cost
FROM DRILLING_PHASE_DETAILS
WHERE actual_cost > (SELECT AVG(actual_cost) FROM DRILLING_PHASE_DETAILS)
ORDER BY actual_cost DESC;""",
            "limit": 5
        },
        "S2_E1B": {
            "sql": """SELECT dpd1.drilling_phase_id, dpd1.well_phase_id, dpd1.actual_cost
FROM DRILLING_PHASE_DETAILS dpd1
WHERE dpd1.actual_cost > (
    SELECT AVG(dpd2.actual_cost) 
    FROM DRILLING_PHASE_DETAILS dpd2 
    WHERE dpd2.well_phase_id = dpd1.well_phase_id
)
ORDER BY dpd1.well_phase_id, dpd1.actual_cost DESC;""",
            "limit": 5
        },
        "S2_E2": {
            "sql": """SELECT r.rig_name, s.total_wells
FROM RIG r
JOIN (
    SELECT rig_id, COUNT(well_id) as total_wells
    FROM WELL
    GROUP BY rig_id
) AS s ON r.rig_id = s.rig_id
ORDER BY s.total_wells DESC;"""
        },
        "S2_E3": {
            "sql": """WITH CombinedCosts AS (
    SELECT well_phase_id, actual_cost FROM DRILLING_PHASE_DETAILS
    UNION ALL
    SELECT well_phase_id, actual_cost FROM COMPLETION_PHASE_DETAILS
)
SELECT w.well_name, r.rig_name, ROUND(SUM(cc.actual_cost), 2) as total_actual_cost
FROM CombinedCosts cc
JOIN WELL_PHASE wp ON cc.well_phase_id = wp.well_phase_id
JOIN WELL w ON wp.well_id = w.well_id
JOIN RIG r ON w.rig_id = r.rig_id
GROUP BY w.well_name, r.rig_name
ORDER BY total_actual_cost DESC;"""
        },
        "S2_E4": {
            "sql": """SELECT * FROM MV_WELL_COST_SUMMARY
ORDER BY total_actual_cost DESC;""",
            "setup": """DROP TABLE IF EXISTS MV_WELL_COST_SUMMARY;
CREATE TABLE MV_WELL_COST_SUMMARY AS
SELECT w.well_name, r.rig_name, ROUND(SUM(actual_cost), 2) as total_actual_cost
FROM DRILLING_PHASE_DETAILS dpd
JOIN WELL_PHASE wp ON dpd.well_phase_id = wp.well_phase_id
JOIN WELL w ON wp.well_id = w.well_id
JOIN RIG r ON w.rig_id = r.rig_id
GROUP BY w.well_name, r.rig_name;"""
        },
        "EX_2_1": {
            "sql": """SELECT well_name 
FROM WELL 
WHERE well_id NOT IN (
    SELECT DISTINCT wp.well_id 
    FROM WELL_PHASE wp
    JOIN REPORT_JOURNAL rj ON wp.well_phase_id = rj.well_phase_id
);"""
        },
        "S3_E1": {
            "sql": """SELECT r.rig_name, w.well_name,
       ROW_NUMBER() OVER (PARTITION BY r.rig_id ORDER BY w.well_name) as well_seq
FROM RIG r
JOIN WELL w ON r.rig_id = w.rig_id
ORDER BY r.rig_name, w.well_name;"""
        },
        "S3_E2": {
            "sql": """WITH WellCosts AS (
    SELECT wp.well_id, SUM(dpd.actual_cost) as total_cost
    FROM WELL_PHASE wp
    JOIN DRILLING_PHASE_DETAILS dpd ON wp.well_phase_id = dpd.well_phase_id
    GROUP BY wp.well_id
)
SELECT w.well_name, ROUND(wc.total_cost, 2) as total_cost,
       RANK() OVER (ORDER BY wc.total_cost DESC) as cost_rank,
       DENSE_RANK() OVER (ORDER BY wc.total_cost DESC) as cost_dense_rank
FROM WellCosts wc
JOIN WELL w ON wc.well_id = w.well_id;"""
        },
        "S3_E3": {
            "sql": """SELECT w.well_name, rj.report_datetime, dpd.actual_cost,
       ROUND(SUM(dpd.actual_cost) OVER (
           PARTITION BY w.well_id 
           ORDER BY rj.report_datetime
       ), 2) as cumulative_cost
FROM DRILLING_PHASE_DETAILS dpd
JOIN REPORT_JOURNAL rj ON dpd.report_journal_id = rj.report_journal_id
JOIN WELL_PHASE wp ON dpd.well_phase_id = wp.well_phase_id
JOIN WELL w ON wp.well_id = w.well_id
ORDER BY w.well_name, rj.report_datetime;""",
            "limit": 5
        },
        "S4_E1": {
            "sql": """SELECT well_phase_id, report_datetime, report_type, COUNT(*) as occurrence_count
FROM REPORT_JOURNAL
GROUP BY well_phase_id, report_datetime, report_type
HAVING COUNT(*) > 1;"""
        },
        "S4_E2": {
            "sql": """SELECT dpd.drilling_phase_id, dpd.well_phase_id, dpd.report_journal_id, dpd.actual_cost
FROM DRILLING_PHASE_DETAILS dpd
LEFT JOIN REPORT_JOURNAL rj ON dpd.report_journal_id = rj.report_journal_id
WHERE rj.report_journal_id IS NULL;"""
        },
        "S4_E3": {
            "sql": """SELECT drilling_phase_id, well_phase_id, plan_cost, actual_cost,
       COALESCE(actual_cost, plan_cost) as resolved_cost
FROM DRILLING_PHASE_DETAILS
WHERE actual_cost IS NULL
LIMIT 5;"""
        }
    }

    # 2. Formatting helpers
    def format_val(col_name, val):
        if val is None:
            return 'NULL'
        if 'cost' in col_name.lower() and isinstance(val, (int, float)):
            return f"${val:,.2f}"
        return str(val)

    def to_html(headers, rows, limit=None):
        if not rows:
            return f"""<table style="width: 100%; border-collapse: collapse; text-align: left; font-size: 0.85rem; color: var(--color-text-secondary); margin-top: 0.5rem;">
    <thead>
        <tr style="border-bottom: 1px solid rgba(255,255,255,0.1); color: white;">
            {"".join(f'<th style="padding: 0.5rem;">{h}</th>' for h in headers)}
        </tr>
    </thead>
    <tbody>
        <tr><td colspan="{len(headers)}" style="padding: 0.5rem; text-align: center; color: var(--color-text-muted);">No rows returned</td></tr>
    </tbody>
</table>"""
        total = len(rows)
        disp = rows[:limit] if limit else rows
        out = ['<table style="width: 100%; border-collapse: collapse; text-align: left; font-size: 0.85rem; color: var(--color-text-secondary); margin-top: 0.5rem;">']
        out.append('    <thead>')
        out.append('        <tr style="border-bottom: 1px solid rgba(255,255,255,0.1); color: white;">')
        for h in headers:
            out.append(f'            <th style="padding: 0.5rem;">{h}</th>')
        out.append('        </tr>')
        out.append('    </thead>')
        out.append('    <tbody>')
        for r in disp:
            out.append('        <tr style="border-bottom: 1px dashed rgba(255,255,255,0.05);">')
            for h, v in zip(headers, r):
                fmt = format_val(h, v)
                if fmt == 'NULL':
                    out.append(f'            <td style="padding: 0.5rem; color: var(--color-text-muted); font-style: italic;">{fmt}</td>')
                else:
                    out.append(f'            <td style="padding: 0.5rem;">{fmt}</td>')
            out.append('        </tr>')
        if limit and total > limit:
            out.append('        <tr>')
            out.append(f'            <td colspan="{len(headers)}" style="padding: 0.5rem; text-align: center; color: var(--color-text-muted); font-style: italic;">... and {total - limit} more rows</td>')
            out.append('        </tr>')
        out.append('    </tbody>')
        out.append('</table>')
        return "\n".join(out)

    def to_md(headers, rows, limit=None):
        if not rows:
            return "| " + " | ".join(headers) + " |\n| " + " | ".join(":---" for _ in headers) + " |\n| " + "No rows returned" + " |" + " |" * (len(headers) - 1) + " |"
        total = len(rows)
        disp = rows[:limit] if limit else rows
        out = []
        out.append("| " + " | ".join(headers) + " |")
        out.append("| " + " | ".join(":---" for _ in headers) + " |")
        for r in disp:
            out.append("| " + " | ".join(format_val(h, v) for h, v in zip(headers, r)) + " |")
        if limit and total > limit:
            out.append("| " + f"*[... and {total - limit} more rows]*" + " |" + " |" * (len(headers) - 1) + " |")
        return "\n".join(out)

    # 3. Read files
    try:
        with open(html_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
    except FileNotFoundError:
        html_content = None

    try:
        with open(md_path, 'r', encoding='utf-8') as f:
            md_content = f.read()
    except FileNotFoundError:
        md_content = None

    # 4. Process queries and update files
    for key, q_info in queries.items():
        if "setup" in q_info:
            for stmt in q_info["setup"].split(";"):
                if stmt.strip():
                    cursor.execute(stmt)
        cursor.execute(q_info["sql"])
        headers = [d[0] for d in cursor.description]
        rows = cursor.fetchall()
        limit = q_info.get("limit")
        
        if html_content and key != "EX_2_1":
            html_table = to_html(headers, rows, limit)
            pattern = rf"(<!--\s*BEGIN_RESULT_{key}\s*-->).*?(<!--\s*END_RESULT_{key}\s*-->)"
            html_content = re.sub(pattern, rf"\1\n{html_table}\n\2", html_content, flags=re.DOTALL)
            
        if md_content:
            md_table = to_md(headers, rows, limit)
            pattern = rf"(<!--\s*BEGIN_RESULT_{key}\s*-->).*?(<!--\s*END_RESULT_{key}\s*-->)"
            md_content = re.sub(pattern, rf"\1\n{md_table}\n\2", md_content, flags=re.DOTALL)

    # 5. Write back updated contents
    if html_content:
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        print("Synchronized index.html example tables successfully.")
        
    if md_content:
        with open(md_path, 'w', encoding='utf-8') as f:
            f.write(md_content)
        print("Synchronized sql_workbook.md example tables successfully.")

if __name__ == "__main__":
    print("Generating drilling_course.db...")
    conn, cursor = create_database()
    populate_data(conn, cursor)
    
    print("Synchronizing static examples in index.html and sql_workbook.md...")
    sync_examples(conn)
    
    print("Updating index.html with new DB data...")
    import json
    import re
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    tables = ['RIG', 'WELL', 'PHASE', 'WELL_PHASE', 'REPORT_JOURNAL', 'DRILLING_PHASE_DETAILS', 'COMPLETION_PHASE_DETAILS']
    db_data = {}
    for t in tables:
        cursor.execute(f"SELECT * FROM {t}")
        rows = cursor.fetchall()
        db_data[t] = [dict(row) for row in rows]
    json_str = json.dumps(db_data, indent=4)
    try:
        with open(html_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        html_content = re.sub(r'const dbData = \{.*?\};', f'const dbData = {json_str};', html_content, flags=re.DOTALL)
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
    except FileNotFoundError:
        print("index.html not found, skipped updating JSON.")

    conn.close()
    print(f"Database generation complete! File saved as '{db_path}'")
