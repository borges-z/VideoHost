from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField
from wtforms.validators import DataRequired, Length, Email, ValidationError
from app import db, bcrypt
from app.modelos import Usuarios

class LoginForm(FlaskForm):
    email = EmailField("E-mail", validators=[DataRequired(), Email()])
    senha = PasswordField("Senha", validators=[DataRequired(), Length(min=3, max=100)])

    def validate_senha(self, senha):
        user = Usuarios.query.filter_by(email=self.email.data).first()
        if not user or not bcrypt.check_password_hash(user.senha, senha.data):
            raise ValidationError("Nome ou email incorreto!")