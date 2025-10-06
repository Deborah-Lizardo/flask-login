from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_user, logout_user, login_required, current_user
from models import User, users  

login = Blueprint("login", __name__, template_folder="templates")


# Página de login
@login.route('/login', methods=['GET'])
def login_page():
    if current_user.is_authenticated:
        return redirect(url_for('home'))  # Se já estiver logado, vai direto para home
    return render_template("login.html")


# Validação de login
@login.route('/validate_user', methods=['POST'])
def validate_user():
    user = request.form['user']
    password = request.form['password']

    if user in users and users[user] == password:
        user_obj = User(user)
        login_user(user_obj, remember=False)  # Sessão temporária
        return redirect(url_for('home'))

    return redirect(url_for('login.login_page'))  # Login falhou, volta para login


# Logout
@login.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login.login_page'))


# Listar usuários
@login.route('/list_users')
@login_required
def list_users():
    return render_template("users.html", users=users)


# Formulário de cadastro
@login.route('/register_user', methods=['GET'])
@login_required
def add_user():
    return render_template("register_user.html")


# Registro de novo usuário
@login.route('/register_user', methods=['POST'])
@login_required
def register_user():
    username = request.form['user']
    password = request.form['password']

    if username in users:
        return redirect(url_for('login.add_user'))

    users[username] = password
    return redirect(url_for('home'))



# chamada da tela de remoção de usuário
@login.route('/remove_user')
@login_required
def remove_user():
    return render_template("remove_user.html", users=users)


# Remoção de usuário em si (post)
@login.route('/del_user', methods=['POST'])
@login_required
def del_user():
    user_to_remove = request.form['user']
    if user_to_remove in users:
        users.pop(user_to_remove)
    return render_template("users.html", users=users)
