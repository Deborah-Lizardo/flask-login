from flask import Flask, render_template, redirect, url_for
from flask_login import LoginManager, login_required, current_user, UserMixin
from auth_routes import login
from models import User, users
from sensors import sensors_bp
from actuators import actuators_bp

# Initialize Flask app
app = Flask(__name__)

# Secret key for session handling
import os, base64
app.secret_key = base64.b64encode(os.urandom(24)).decode('utf-8')

# Setup Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login.login_page'  # Redirect if not logged in

# Reload user from session
@login_manager.user_loader
def load_user(user_id):
    print(f"Loading user with id: {user_id}")
    if user_id is None:
        return None
    if user_id in users:
        return User(user_id)
    return None

# Register blueprints for login, sensors and actuators
app.register_blueprint(login)  # No prefix for login routes
app.register_blueprint(sensors_bp, url_prefix='/sensors')
app.register_blueprint(actuators_bp, url_prefix='/actuators')

# Protected route: home page
@app.route('/home')
@login_required
def home():
    print(f"Accessing home. User authenticated? {current_user.is_authenticated}")
    return render_template("home.html")

# Login route
@app.route('/login')
def login_page():
    return render_template("login.html")

# Redirect to login or home based on authentication
@app.route('/')
def index():
    print(f"User is authenticated: {current_user.is_authenticated}")
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    return redirect(url_for('login.login_page'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
