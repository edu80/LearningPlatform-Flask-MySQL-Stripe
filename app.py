from flask import Flask, render_template, request, jsonify, redirect, url_for, redirect, session
import mysql.connector
import stripe
import json

app = Flask(__name__)

app.secret_key = '#EthioCode@Admin2023'  

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Etagu@1980',
    'database': 'learning_platform'
}

# Helper function to connect to the database
def get_database_connection():
    try:
        connection = mysql.connector.connect(**db_config)
        return connection
    except mysql.connector.Error as err:
        print("Error connecting to the database:", err)
        return None



# Route to serve the index.html (homepage)
@app.route('/')
def serve_index_page():
    return render_template('index.html')

# Route to serve the registration form
@app.route('/registration.html')
def serve_registration_form():
    return render_template('registration.html')

# Route to serve the login form
@app.route('/login.html')
def serve_login_form():
    return render_template('login.html')





# Route to handle user registration
@app.route('/register', methods=['POST'])
def register_user():
    # Retrieve form data from AJAX request
    name = request.form.get('name')
    email = request.form.get('email')
    password = request.form.get('password')

    # Perform registration logic (e.g., store user data in the database)
    connection = get_database_connection()
    if connection is None:
        return jsonify({'message': 'Error connecting to the database'}), 500

    try:
        cursor = connection.cursor()
        # Check if the email already exists in the database
        check_query = "SELECT email FROM users WHERE email = %s"
        cursor.execute(check_query, (email,))
        existing_email = cursor.fetchone()

        if existing_email:
            # If the email already exists, return a response indicating that the email is already registered
            cursor.close()
            connection.close()
            return jsonify({'message': 'Email already registered'}), 400

        # If the email is not registered, proceed with the registration
        insert_query = "INSERT INTO users (name, email, password) VALUES (%s, %s, %s)"
        cursor.execute(insert_query, (name, email, password))
        connection.commit()
        cursor.close()
        connection.close()
        return jsonify({'message': 'Registration successful'}), 200

    except mysql.connector.Error as err:
        print("Error executing SQL query:", err)
        connection.rollback()
        cursor.close()
        connection.close()
        return jsonify({'message': 'Error during registration'}), 500


# Route to handle user login
@app.route('/login', methods=['POST'])
def login_user():
    # Your login logic here
    # Retrieve form data from AJAX request
    email = request.form.get('email')
    password = request.form.get('password')

    # Perform login logic (e.g., validate credentials against the database)
    connection = get_database_connection()
    if connection is None:
        return jsonify({'message': 'Error connecting to the database'}), 500

    try:
        cursor = connection.cursor()
        # Replace 'users' with your actual table name for storing user data
        select_query = "SELECT id, name, email FROM users WHERE email = %s AND password = %s"
        cursor.execute(select_query, (email, password))
        user_data = cursor.fetchone()
        cursor.close()
        connection.close()

        if user_data is not None:
            # Login successful, store the user_id in the session
            session['user_id'] = user_data[0]
            return jsonify({'message': 'Login successful', 'redirect': url_for('dashboard')}), 200
        else:
            # Invalid credentials, return an error response
            return jsonify({'message': 'Invalid credentials'}), 401

    except mysql.connector.Error as err:
        print("Error executing SQL query:", err)
        connection.rollback()
        cursor.close()
        connection.close()
        return jsonify({'message': 'Error during login'}), 500


# Route to handle user logout
@app.route('/logout', methods=['POST'])
def logout_user():
    # Perform logout logic (e.g., clear session, cookies, etc.)
    # Then, redirect the user to 'index.html'
    # For example, to clear the session and redirect to 'index.html', you can do:
    # session.clear()  # Make sure you import 'session' from Flask's session module
    return render_template('index.html')

# Function to fetch user data from the database
def get_user_data():
    user_id = session.get('user_id')  # Assuming you have stored the user_id in the session after login
    if user_id:
        try:
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor()
            query = "SELECT name, email FROM users WHERE id = %s"
            cursor.execute(query, (user_id,))
            user_data = cursor.fetchone()
            cursor.close()
            conn.close()
            return user_data
        except mysql.connector.Error as err:
            print(f"Error: {err}")
    return None

# Route to serve the dashboard page
@app.route('/dashboard.html')
def dashboard():
    # Check if the user is logged in (i.e., user_id is in the session)
    if 'user_id' in session:
        user_data = get_user_data()
        if user_data:
            user_name, user_email = user_data
            return render_template('dashboard.html', user_name=user_name, user_email=user_email)
    
    # If the user is not logged in or data retrieval failed, redirect them to the login page
    return redirect('/login')


# Route to get the Stripe publishable key
@app.route("/get_stripe_publishable_key")
def get_stripe_publishable_key():
    # Replace 'stripe_secret_key' with your actual Stripe secret key
    stripe_secret_key = "sk_test_51NVIiDDv1EHH4dE05IdtQAFv4U8WSfV8OpyxIPcJR9SuG5Uc5kWBni6FTq5aCjyz45YSM8rXJISkNJIxjAzMpxCs00svPHqUZ8"
    return jsonify({"publishableKey": stripe_secret_key})

# Route to handle the payment session creation
@app.route('/create_payment_session', methods=['POST'])
def create_payment_session():
    try:
        # Retrieve payment information from the client (e.g., amount, currency, etc.)
        # You can use request.form or request.json to get the data sent from the client

        # Create a Stripe payment session
        stripe.api_key = "sk_test_51NVIiDDv1EHH4dE05IdtQAFv4U8WSfV8OpyxIPcJR9SuG5Uc5kWBni6FTq5aCjyz45YSM8rXJISkNJIxjAzMpxCs00svPHqUZ8"  # Replace with your actual Stripe secret key
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price': 'price_XXXXX',  # Replace with the actual price ID from Stripe Dashboard
                    'quantity': 1,
                },
            ],
            mode='payment',
            success_url='https://your-domain.com/success',  # Replace with your actual success URL
            cancel_url='https://your-domain.com/cancel',    # Replace with your actual cancel URL
        )

        # Return the session ID to the client
        return jsonify({'sessionId': session['id']})
    except stripe.error.StripeError as e:
        return jsonify({'error': 'Error creating payment session'}), 500


# Route to serve the checkout.html file
@app.route('/checkout.html')
def serve_checkout_page():
    return render_template('checkout.html')

# Route to handle the redirect from index.html to checkout.html
@app.route('/checkout', methods=['GET'])
def redirect_to_checkout():
    return redirect(url_for('serve_checkout_page'))

# Route to handle webhook events (optional, for handling payment success or failure)

@app.route('/webhook', methods=['POST'])
def webhook():
    payload = request.data
    event = None

    try:
        event = stripe.Event.construct_from(
            json.loads(payload), stripe.api_key
        )
    except ValueError as e:
        return jsonify({'error': 'Invalid payload'}), 400

    # Handle the event (e.g., update the database, send confirmation email, etc.)
    # For example, you can check the event type and status to update your database accordingly.

    return jsonify({'status': 'success'}), 200



if __name__ == "__main__":
    app.run(debug=True)