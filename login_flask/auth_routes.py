# Renamed from 'login.py' to 'auth_routes.py' to avoid conflict with Flask-Login's internal 'login' name
# Flask-Login internally uses 'login' as a reference (e.g., login_manager.login_view = 'login'),
# which was causing routing and import issues when our file was also named 'login.py'.

from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_user, logout_user, login_required, current_user
from models import User, users  

# Create Blueprint for authentication routes
login = Blueprint("login", __name__, template_folder="templates")

# Login page (GET)
@login.route('/login', methods=['GET'])
def login_page():
    if current_user.is_authenticated:
        return redirect(url_for('home'))  # Redirect to home if already logged in
    return render_template("login.html")

# Handle login form submission (POST)
@login.route('/validate_user', methods=['POST'])
def validate_user():
    user = request.form['user']
    password = request.form['password']

    if user in users and users[user] == password:
        user_obj = User(user)
        login_user(user_obj, remember=False)  # Start session for user
        return redirect(url_for('home'))

    return redirect(url_for('login.login_page'))  # Invalid login

# Logout route
@login.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login.login_page'))

# List all registered users
@login.route('/list_users')
@login_required
def list_users():
    return render_template("users.html", users=users)

# Show user registration form (GET)
@login.route('/register_user', methods=['GET'])
@login_required
def add_user():
    return render_template("register_user.html")

# Handle user registration form submission (POST)
@login.route('/register_user', methods=['POST'])
@login_required
def register_user():
    username = request.form['user']
    password = request.form['password']

    if username in users:
        return redirect(url_for('login.add_user'))  # User already exists

    users[username] = password
    return redirect(url_for('home'))

# Show user deletion form
@login.route('/remove_user')
@login_required
def remove_user():
    return render_template("remove_user.html", users=users)

# Handle user deletion (POST)
@login.route('/del_user', methods=['POST'])
@login_required
def del_user():
    user_to_remove = request.form['user']
    if user_to_remove in users:
        users.pop(user_to_remove)
    return render_template("users.html", users=users)