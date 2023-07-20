from flask import Flask, request, render_template
import mysql.connector

app = Flask(__name__)

# Establish a connection to the MySQL database
cnx = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Etagu@1980",
    database="learning_platform"
)

# Handle registration form submission
@app.route('/register', methods=['POST'])
def register_user():
    name = request.form.get('name')
    email = request.form.get('email')
    password = request.form.get('password')

    cursor = cnx.cursor()
    insert_query = "INSERT INTO users (name, email, password) VALUES (%s, %s, %s)"
    user_data = (name, email, password)
    cursor.execute(insert_query, user_data)
    cnx.commit()
    cursor.close()

    # Close the database connection
    cnx.close()

    return "Registration successful"

# Serve the registration form
@app.route('/')
def serve_registration_form():
    return render_template('registration.html')

if __name__ == '__main__':
    app.run()
