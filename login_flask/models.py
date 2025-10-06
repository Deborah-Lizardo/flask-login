from flask_login import UserMixin
users = {
    "deborah": "14082001",
    "ana": "124567"
}


class User(UserMixin):
    def __init__(self, id):
        self.id = id  # O id pode ser o username ou um id único (depende da sua implementação)

    def get_id(self):
        return self.id  # Retorna o id do usuário (normalmente username ou user_id)