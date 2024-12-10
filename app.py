from flask import Flask, render_template, request, redirect, url_for , jsonify
import sqlite3
import subprocess

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    conn = get_db_connection()
    rows = conn.execute('SELECT * FROM users').fetchall()
    conn.close()
    return render_template('index.html', rows=rows)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        conn = get_db_connection()
        conn.execute('INSERT INTO users (name, age) VALUES (?, ?)', (name, age))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    return render_template('add.html')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    conn = get_db_connection()
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        conn.execute('UPDATE users SET name = ?, age = ? WHERE id = ?', (name, age, id))
        conn.commit()
    
    user = conn.execute('SELECT * FROM users WHERE id = ?', (id,)).fetchone()
    conn.close()
    return render_template('edit.html', user=user)

@app.route('/get_user/<int:id>', methods=['GET'])
def get_user(id):
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE id = ?', (id,)).fetchone()
    conn.close()
    return {
        'id': user['id'],
        'name': user['name'],
        'age': user['age']
    }

@app.route('/run_command', methods=['POST'])
def run_command():
    command = request.form['command']
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        output = result.stdout if result.returncode == 0 else result.stderr
    except Exception as e:
        output = str(e)
    return jsonify({'output': output})



if __name__ == '__main__':
    app.run(debug=True)
