from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.secret_key = "mude aqui"
bcrypt = Bcrypt(app)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
app.config['VIDEOS_FOLDER'] = "uploads"


db = SQLAlchemy(app)
mi = Migrate(app, db)


from . import rotas
from . import modelos