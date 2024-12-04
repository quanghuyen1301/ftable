import sqlite3

connection = sqlite3.connect('database.db')

with connection:
    connection.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT, age INTEGER)')
    connection.execute('INSERT INTO users (name, age) VALUES ("Alice", 25), ("Bob", 30), ("Charlie", 35)')

connection.close()
