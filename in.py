import sqlite3

# Connect to the database
conn = sqlite3.connect('users.db')
c = conn.cursor()

# Execute a query to select all data from the users table
c.execute("SELECT * FROM users")

# Fetch all rows from the executed query
rows = c.fetchall()

# Print the column names (optional)
column_names = [description[0] for description in c.description]
print(f"Columns: {', '.join(column_names)}")

# Print all rows
for row in rows:
    print(row)

# Close the connection
conn.close()