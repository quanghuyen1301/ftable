from flask import Flask, render_template, request, redirect, url_for
import sqlite3

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

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    conn = get_db_connection()
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        conn.execute('UPDATE users SET name = ?, age = ? WHERE id = ?', (name, age, id))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    else:
        user = conn.execute('SELECT * FROM users WHERE id = ?', (id,)).fetchone()
        conn.close()
        return render_template('edit.html', user=user)

if __name__ == '__main__':
    app.run(debug=True)
