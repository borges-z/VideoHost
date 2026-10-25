from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, Length
from flask_wtf.file import FileField, FileRequired, FileAllowed, FileSize

class VideoForm(FlaskForm):
    titulo = StringField('Titulo', validators=[DataRequired(message="O campo titulo é obrigatório"), Length(min=3, max=80, message="O tamano do titulo deve ser de 3 á 80 caracteres!")])
    video = FileField("Video", validators=[FileRequired(), FileAllowed(['mp4', 'mkv']), FileSize(min_size=50000000, max_size=5000000000)])
