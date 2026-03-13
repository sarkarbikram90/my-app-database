from flask import Flask, render_template, request, redirect, url_for
import psycopg2
from psycopg2.extras import RealDictCursor
import os
from dotenv import load_dotenv

# Load the password from the .env file
load_dotenv()

app = Flask(__name__)

# 1. CONNECT TO CLOUD DATABASE
def get_db_connection():
    # We read the URL from the environment variable, not hard-coded
    conn = psycopg2.connect(os.getenv('DATABASE_URL'))
    return conn

# 2. SETUP THE TABLE (Postgres syntax is slightly different from SQLite)
def init_db():
    conn = get_db_connection()
    cur = conn.cursor()
    # 'SERIAL' automatically creates an ID in Postgres
    cur.execute('''
        CREATE TABLE IF NOT EXISTS employees (
            id SERIAL PRIMARY KEY,
            name TEXT NOT NULL,
            age INTEGER NOT NULL,
            country TEXT NOT NULL,
            salary REAL NOT NULL
        )
    ''')
    conn.commit()
    cur.close()
    conn.close()

# 3. THE WEBPAGE
@app.route('/')
def index():
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute('SELECT * FROM employees')
    employees = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('index.html', employees=employees)

# 4. HANDLE FORM SUBMISSION
@app.route('/add', methods=['POST'])
def add_employee():
    name = request.form['name']
    age = request.form['age']
    country = request.form['country']
    salary = request.form['salary']

    conn = get_db_connection()
    cur = conn.cursor()
    # %s is the placeholder for Postgres (SQLite used ?)
    cur.execute('INSERT INTO employees (name, age, country, salary) VALUES (%s, %s, %s, %s)',
                (name, age, country, salary))
    conn.commit()
    cur.close()
    conn.close()
    
    return redirect(url_for('index'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)