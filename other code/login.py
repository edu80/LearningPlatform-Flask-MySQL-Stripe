#!/usr/bin/env python3
import cgi
import mysql.connector

# Establish a connection to the MySQL database
cnx = mysql.connector.connect(
  host="localhost",
  user="root",
  password="Etagu@1980",
  database="learning_platform"
)

# Handle login form submission
def login_user(email, password):
  cursor = cnx.cursor()
  select_query = "SELECT * FROM users WHERE email = %s AND password = %s"
  user_data = (email, password)
  cursor.execute(select_query, user_data)
  user = cursor.fetchone()
  cursor.close()

  if user:
    # Login successful
    print("Content-Type: text/html")
    print()
    print("Login successful")  # or return an appropriate message
  else:
    # Invalid email or password
    print("Content-Type: text/html")
    print()
    print("Invalid email or password")  # or return an appropriate message

# Retrieve form data from the request
form = cgi.FieldStorage()
email = form.getvalue("email")
password = form.getvalue("password")

# Perform form validation if needed

# Call the login_user function
login_user(email, password)

# Close the database connection
cnx.close()

# Send a response back to the client if needed
