import sqlite3
connection = sqlite3.connect('data.db')
cursor = connection.cursor()


# use INTEGER (full word, not "int") to make auto-incrementing ID values
create_table = "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username test, password text)"
cursor.execute(create_table)

create_table = "CREATE TABLE IF NOT EXISTS items (name text, price real)"
cursor.execute("INSERT INTO items VALUES ('test': 10.99)")

connection.commit()

connection.close()
