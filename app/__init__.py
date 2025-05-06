from flask import Flask, redirect, url_for
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from app.config.app_config import APP_CONFIG
from flasgger import Swagger
from flask_migrate import Migrate
from authlib.integrations.flask_client import OAuth
from flask_mail import Mail
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)
app.config.from_object(APP_CONFIG)
swagger = Swagger(app)

oauth = OAuth(app)

db = SQLAlchemy(app)
migrate = Migrate(app, db)
jwt = JWTManager(app)
oauth = OAuth(app)
mail = Mail(app)

# FAÇA O REGISTRO DA MODEL AQUI PARA ELA SER CRIADA NO BANCO DE DADOS COM O COMANDO ABAIXO
# NAO ESQUECA DE CRIAR O BANCO DE DADOS ANTES
# FLASK DB MIGRATE -M "MESSAGE TEXT"
# FLASK DB UPGRADE
# CUIDADO AO FAZER MIGRATE 
from app.models import Sensor, Turbidez, Perfil, Usuario, Propriedade

from app.controllers import turbidez_controller, perfil_controller, usuario_controller, auth_controller, propriedade_controller

app.add_url_rule('/leitura/turbidez', 'salvar_turbidez', turbidez_controller.salvar_turbidez, methods=['POST'])
app.add_url_rule('/perfil', 'salvar_perfil', perfil_controller.salvar_perfil, methods=['POST'])
app.add_url_rule('/perfil', 'listar_perfil', perfil_controller.listar_perfil, methods=['GET'])
app.add_url_rule('/perfil/<string:id>','atualizar_perfil', perfil_controller.atualizar_perfil, methods=['PUT'])
app.add_url_rule('/perfil/<string:id>','deletar_perfil', perfil_controller.deletar_perfil, methods=['DELETE'])
app.add_url_rule('/perfil/<string:id>','buscar_perfil', perfil_controller.buscar_perfil, methods=['GET'])
app.add_url_rule('/usuarios', 'salvar_usuario', usuario_controller.salvar_usuario, methods=['POST'])
app.add_url_rule('/usuarios', 'listar_usuarios', usuario_controller.listar_usuarios, methods=['GET'])
app.add_url_rule('/usuarios/<string:id>', 'atualizar_usuario', usuario_controller.atualizar_usuario, methods=['PUT'])
app.add_url_rule('/usuarios/<string:id>', 'status_usuario', usuario_controller.status_usuario, methods=['PATCH'])
app.add_url_rule('/usuarios/<string:id>', 'buscar_usuario', usuario_controller.buscar_usuario, methods=['GET'])
app.add_url_rule('/usuarios/relatorio', 'relatorio_usuarios', usuario_controller.relatorio_usuarios, methods=['GET'])
app.add_url_rule('/register', 'register', auth_controller.register, methods=['POST'])
app.add_url_rule('/login', 'login', auth_controller.login, methods=['POST'])
app.add_url_rule('/refresh', 'refresh_token', auth_controller.refresh_token, methods=['POST'])
app.add_url_rule('/forgot-password', 'reset_password_request', auth_controller.reset_password_request, methods=['POST'])
app.add_url_rule('/reset-password', 'reset_password', auth_controller.reset_password, methods=['POST'])
# app.add_url_rule('/login/google', 'login_google', auth_controller.login_google, methods=['GET']) DESATIVADO, RESPONSABILIDADE DO FRONTEND PARA FAZER O LOGIN
app.add_url_rule('/login/google', 'authorize_google', auth_controller.authorize_google,  methods=['POST'])
app.add_url_rule('/propriedade', 'cadastrar_propriedade', propriedade_controller.cadastrar_propriedade, methods=['POST'])
app.add_url_rule('/propriedade', 'listar_propriedades', propriedade_controller.listar_propriedades, methods=['GET'])
app.add_url_rule('/propriedade/<string:id>', 'atualizar_propriedade', propriedade_controller.atualizar_propriedade, methods=['PUT'])
app.add_url_rule('/propriedade/<string:id>', 'detalhar_propriedade', propriedade_controller.detalhar_propriedade, methods=['GET'])
app.add_url_rule('/propriedade/usuarios/adicionar', 'adicionar_usuario', propriedade_controller.adicionar_usuario, methods=['POST'])
app.add_url_rule('/propriedade/usuarios/remover', 'remover_usuario', propriedade_controller.remover_usuario, methods=['POST'])
app.add_url_rule('/propriedade/usuarios/convidar', 'convidar_usuario', propriedade_controller.convidar_usuario, methods=['POST'])
app.add_url_rule('/propriedade/usuarios/convidar/aceitar', 'convite_aceito', propriedade_controller.convite_aceito, methods=['POST'])
app.add_url_rule('/propriedade/usuarios/perfil', 'atualizar_perfil_local', propriedade_controller.atualizar_perfil_local, methods=['POST'])
app.add_url_rule('/propriedade/perfil', 'salvar_perfil_local', propriedade_controller.salvar_perfil_local, methods=['POST'])



@app.route('/')
def home():
    return redirect(url_for('flasgger.apidocs'))

