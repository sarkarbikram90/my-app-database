from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)
DB_NAME = "employees.db"

# 1. FUNCTION TO CONNECT TO DATABASE
def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row  # This allows us to access columns by name
    return conn

# 2. SETUP THE DATABASE TABLE (Runs once when app starts)
def init_db():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER NOT NULL,
            country TEXT NOT NULL,
            salary REAL NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# 3. THE WEBPAGE (Show form and list existing data)
@app.route('/')
def index():
    conn = get_db_connection()
    employees = conn.execute('SELECT * FROM employees').fetchall()
    conn.close()
    return render_template('index.html', employees=employees)

# 4. HANDLE FORM SUBMISSION (Add data to DB)
@app.route('/add', methods=['POST'])
def add_employee():
    name = request.form['name']
    age = request.form['age']
    country = request.form['country']
    salary = request.form['salary']

    conn = get_db_connection()
    # This is the magic line that sends data to the DB
    conn.execute('INSERT INTO employees (name, age, country, salary) VALUES (?, ?, ?, ?)',
                 (name, age, country, salary))
    conn.commit()
    conn.close()
    
    return redirect(url_for('index'))

if __name__ == '__main__':
    init_db() # Create table if it doesn't exist
    app.run(debug=True)