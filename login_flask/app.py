from flask import Flask, render_template, redirect, url_for
from flask_login import LoginManager, login_required, current_user,UserMixin
from auth_routes import login
from models import User, users
from sensors import sensors_bp
from actuators import actuators_bp

#Segunda parte: configuração do flask login
app = Flask(__name__) #Cria instancia do app
import os, base64
app.secret_key = base64.b64encode(os.urandom(24)).decode('utf-8')

#Inicializando o flask-login
login_manager = LoginManager()
login_manager.init_app(app)

login_manager.login_view = 'login.login_page'

#Função user loader
#É chamada sempre p saber quem é o usuário atual(recuperar o id)
#This callback is used to reload the user object from the user ID stored in the session.
@login_manager.user_loader
def load_user(user_id):
    print(f"Loading user with id: {user_id}")  # Para debug
    if user_id is None:
        return None
    if user_id in users:
        return User(user_id)
    return None


#parte de bp- terceira parte
app.register_blueprint(login)  # sem url_prefix
app.register_blueprint(sensors_bp, url_prefix='/sensors')
app.register_blueprint(actuators_bp, url_prefix='/actuators')

#Parte 4 rotas protegidas com required
@app.route('/home')
@login_required
def home():
    print(f"Accessing home. User authenticated? {current_user.is_authenticated}")
    return render_template("home.html")


@app.route('/login')
def login_page():
    return render_template("login.html")  # Página de login

@app.route('/')
def index():
    print(f"User is authenticated: {current_user.is_authenticated}")  # Para depuração
    if current_user.is_authenticated: 
        return redirect(url_for('home'))  
    return redirect(url_for('login.login_page')) 


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
