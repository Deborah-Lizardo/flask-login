from flask import Blueprint, render_template, request
from flask_login import login_required

# Blueprint for sensor-related routes
sensors_bp = Blueprint('sensors', __name__, template_folder="templates")

# In-memory sensor dictionary (example data)
sensors = {'temperature': 23, 'humidity': 22, 'luminosity': 10}

# List all sensors (GET)
@sensors_bp.route('/sensors')
@login_required
def list_sensors():
    return render_template("sensors.html", sensors=sensors)

# Form to register a new sensor (GET)
@sensors_bp.route('/add_sensor', methods=['GET'])
@login_required
def add_sensor():
    return render_template("register_sensor.html")

# Register sensor (POST) or show form again (GET)
@sensors_bp.route('/register_sensor', methods=['GET', 'POST'])
def register_sensor():
    global sensors
    if request.method == 'POST':
        sensor_name = request.form['sensor']
        sensor_value = request.form['value']
        sensors[sensor_name] = int(sensor_value)
        return render_template("sensors.html", sensors=sensors)
    else:
        return render_template("register_sensor.html")

# Show form to delete a sensor (GET)
@sensors_bp.route('/del_sensor')
def del_sensor():
    return render_template("remove_sensor.html", sensors=sensors)

# Remove sensor from dictionary (POST)
@sensors_bp.route('/remove_sensor', methods=['POST'])
@login_required
def remove_sensor():
    sensor_to_remove = request.form['sensor']
    if sensor_to_remove in sensors:
        sensors.pop(sensor_to_remove)
    return render_template("sensors.html", sensors=sensors)
