from flask_login import UserMixin

# Hardcoded user database: dictionary where key = username, value = password
users = {
    "deborah": "14082001",
    "ana": "124567"
}

# Custom User class required by Flask-Login
class User(UserMixin):
    def __init__(self, id):
        self.id = id 

    def get_id(self):
        return self.id  # Required by Flask-Login to identify the user