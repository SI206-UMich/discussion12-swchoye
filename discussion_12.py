import unittest
import sqlite3
import json
import os
import matplotlib.pyplot as plt
# starter code

# Create Database
def setUpDatabase(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn


# TASK 1
# CREATE TABLE FOR EMPLOYEE INFORMATION IN DATABASE AND ADD INFORMATION
def create_employee_table(cur, conn):
    
    cur.execute("CREATE TABLE IF NOT EXISTS  employees (employee_id INTEGER PRIMARY KEY, first_name TEXT, last_name TEXT, job_id INTEGER, hire_date DATE, salary INTEGER)")

    conn.commit()

# ADD EMPLOYEE'S INFORMTION TO THE TABLE

def add_employee(filename, cur, conn):
    #load .json file and read job data
    # WE GAVE YOU THIS TO READ IN DATA
    f = open(os.path.abspath(os.path.join(os.path.dirname(__file__), filename)))
    file_data = f.read()
    f.close()
    # THE REST IS UP TO YOU
    insert = []
    id_set = set()

    file_data = json.loads(file_data)
    
    for info in file_data:
        id = info["employee_id"] 
        if id in id_set:
            continue
        id_set.add(id)
        
        first_name = info["first_name"]
        last_name = info["last_name"]
        hire_date = info["hire_date"]
        job_id = info["job_id"]
        salary = info["salary"]
        
        insert.append((id, first_name, last_name, job_id, hire_date, salary))       
    cur.executemany("INSERT OR IGNORE INTO  employees VALUES(?,?,?,?,?,?)", insert)
    
    
    conn.commit()
    
    pass

# TASK 2: GET JOB AND HIRE_DATE INFORMATION
def job_and_hire_date(cur, conn):
    
    res = cur.execute("SELECT job_title FROM employees INNER JOIN jobs USING (job_id) order by hire_date")
    return res.fetchone()[0]
# TASK 3: IDENTIFY PROBLEMATIC SALARY DATA
# Apply JOIN clause to match individual employees
def problematic_salary(cur, conn):
    
    res = cur.execute("SELECT first_name, last_name FROM employees INNER JOIN jobs USING (job_id) WHERE (salary > max_salary) OR (salary < min_salary)")
    return res.fetchall()
    
# TASK 4: VISUALIZATION
def visualization_salary_data(cur, conn):
    
    res2 = cur.execute("SELECT job_title, salary FROM employees INNER JOIN jobs USING (job_id)")
    empx = []
    empy = []
    for points in res2.fetchall():
        x,y = points
        empx.append(x)
        empy.append(y)
    
    plt.scatter(empx, empy)
    
    datax = []
    datay = []
    res1 = cur.execute("SELECT job_title, min_salary, max_salary FROM jobs")
    
    for points in res1.fetchall():
        job_title, min_salary, max_salary = points
        datax.append(job_title)
        datay.append(min_salary)
        datax.append(job_title)
        datay.append(max_salary)
    
    plt.scatter(datax, datay, c = 'r', marker = 'x')
    plt.xticks(rotation=45)
    
    
   
    
    plt.show()
    
class TestDiscussion12(unittest.TestCase):
    def setUp(self) -> None:
        self.cur, self.conn = setUpDatabase('HR.db')

    def test_create_employee_table(self):
        self.cur.execute("SELECT COUNT(*) FROM sqlite_master WHERE type='table' AND name='employees'")
        table_check = self.cur.fetchall()[0][0]
        self.assertEqual(table_check, 1, "Error: 'employees' table was not found")
        self.cur.execute("SELECT * FROM employees")
        count = len(self.cur.fetchall())
        self.assertEqual(count, 13)

    def test_job_and_hire_date(self):
        self.assertEqual('President', job_and_hire_date(self.cur, self.conn))

    def test_problematic_salary(self):
        sal_list = problematic_salary(self.cur, self.conn)
        self.assertIsInstance(sal_list, list)
        self.assertEqual(sal_list[0], ('Valli', 'Pataballa'))
        self.assertEqual(len(sal_list), 4)
        
    def test_visualization(self):
        visualization_salary_data(self.cur, self.conn)
def main():
    # SETUP DATABASE AND TABLE
    cur, conn = setUpDatabase('HR.db')
    create_employee_table(cur, conn)

    add_employee("employee.json",cur, conn)

    job_and_hire_date(cur, conn)

    wrong_salary = (problematic_salary(cur, conn))
    print(wrong_salary)

if __name__ == "__main__":
    main()
    unittest.main(verbosity=2)
