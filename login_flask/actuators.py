from flask import Blueprint, render_template, request
from flask_login import login_required

actuators_bp = Blueprint('actuators', __name__, template_folder="templates")

actuators = {'lamp':1, 'serv motor':122}

#"home" dos actuators
@actuators_bp.route('/actuators')
@login_required
def list_actuators():
    return render_template("actuators.html", actuators=actuators)

#create
#chamada = register e metodo add
@actuators_bp.route('/register_actuator')
@login_required
def register_actuator():
    return render_template("register_actuators.html")

@actuators_bp.route('/add_actuator', methods=['GET', 'POST'])
@login_required
def add_actuator():
    global actuators
    if request.method == 'POST':
        actuator_name = request.form['actuator']
        actuator_value = request.form['value']
        actuators[actuator_name] = int(actuator_value)
        return render_template("actuators.html", actuators=actuators)
    else:
        return render_template("register_actuators.html")


#read
@actuators_bp.route('/list_actuators')
@login_required
def actuator():
    return render_template("actuators.html", actuators=actuators)

#delete igual aos sensores
@actuators_bp.route('/del_actuator')
@login_required
def del_actuator():
    return render_template("remove_actuator.html", actuators=actuators)

@actuators_bp.route('/remove_actuator', methods=['POST'])
@login_required
def remove_actuator():
    actuator_to_remove = request.form['actuator']
    if actuator_to_remove in actuators:
        actuators.pop(actuator_to_remove)
    return render_template("actuators.html", actuators=actuators)
