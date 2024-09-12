import sqlite3

conn = sqlite3.connect('users.db')
c = conn.cursor()

c.execute('''
    CREATE TABLE users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        password TEXT NOT NULL,
        ip_address TEXT NOT NULL
    )
''')

conn.commit()
conn.close()
print("Database and table created successfully!")
