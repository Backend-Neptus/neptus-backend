from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app.config.config import Config

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)

from app.controllers import turbidez_controller

app.add_url_rule('/leitura/turbidez', 'salvar_turbidez', turbidez_controller.salvar_turbidez, methods=['POST'])

with app.app_context():
    db.create_all()

