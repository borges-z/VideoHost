from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, PasswordField
from wtforms.validators import DataRequired, Length, Email, ValidationError

class RegistroForm(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired(message="O campo nome é obrigatório"), Length(min=3, max=10, message="O tamano do nome deve ser de 3 á 10 caracteres!")])
    email = EmailField("E-mail", validators=[DataRequired(), Email()])
    senha = PasswordField("Senha", validators=[DataRequired(), Length(min=3, max=100)])

    def validate_nome(self, field):
        if field.data == 'admin':
            raise ValidationError('O nome "admin" não é permitido.')
