from flask import Flask, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from app.config.config import Config
from flasgger import Swagger

app = Flask(__name__)
app.config.from_object(Config)
swagger = Swagger(app)

db = SQLAlchemy(app)

from app.controllers import turbidez_controller

app.add_url_rule('/leitura/turbidez', 'salvar_turbidez', turbidez_controller.salvar_turbidez, methods=['POST'])

@app.route('/')
def home():
    return redirect(url_for('flasgger.apidocs'))

with app.app_context():
    db.create_all()

