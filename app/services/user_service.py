from app import db, bcrypt
from app.modelos import Usuarios


def get_user(id: int):
    return Usuarios.query.filter_by(id=id).first()

def get_user_email(email: str|None):
    return Usuarios.query.filter_by(email=email).first()


def verificar_credenciais(email: str, senha: str):
    user = Usuarios.query.filter_by(email=email).first()
    if user and bcrypt.check_password_hash(user.senha, senha):
        return user
    return None

def registrar_usuario(nome, email, senha):
    user = Usuarios(nome=nome, email=email, senha=senha)
    db.session.add(user)
    db.session.commit()
    return True