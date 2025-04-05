from flask import Flask, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from app.config.config import Config
from flasgger import Swagger
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object(Config)
swagger = Swagger(app)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# FAÇA O REGISTRO DA MODEL AQUI PARA ELA SER CRIADA NO BANCO DE DADOS COM O COMANDO ABAIXO
# NAO ESQUECA DE CRIAR O BANCO DE DADOS ANTES
# FLASK DB MIGRATE -M "MESSAGE TEXT"
# FLASK DB UPGRADE
# CUIDADO AO FAZER MIGRATE 
from app.models import Sensor, Turbidez, Perfil, Usuario

from app.controllers import turbidez_controller, perfil_controller, usuario_controller

app.add_url_rule('/leitura/turbidez', 'salvar_turbidez', turbidez_controller.salvar_turbidez, methods=['POST'])
app.add_url_rule('/perfil', 'salvar_perfil', perfil_controller.salvar_perfil, methods=['POST'])
app.add_url_rule('/perfil', 'listar_perfil', perfil_controller.listar_perfil, methods=['GET'])
app.add_url_rule('/perfil/<int:id>','atualizar_perfil', perfil_controller.atualizar_perfil, methods=['PUT'])
app.add_url_rule('/usuarios', 'salvar_usuario', usuario_controller.salvar_usuario, methods=['POST'])
app.add_url_rule('/usuarios', 'listar_usuarios', usuario_controller.listar_usuarios, methods=['GET'])
app.add_url_rule('/usuarios/<int:id>', 'atualizar_usuario', usuario_controller.atualizar_usuario, methods=['PUT'])


@app.route('/')
def home():
    return redirect(url_for('flasgger.apidocs'))

with app.app_context():
    db.create_all()

