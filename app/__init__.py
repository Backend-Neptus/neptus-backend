from flask import Flask, redirect, url_for
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from app.config.config import Config
from flasgger import Swagger
from flask_migrate import Migrate
from authlib.integrations.flask_client import OAuth
from flask_mail import Mail

app = Flask(__name__)
app.config.from_object(Config)
swagger = Swagger(app)

oauth = OAuth(app)

google = oauth.register(
    name='google',
    client_id='1002584745082-4dhdl28pa57em81klq5kp4ch97b8k5ru.apps.googleusercontent.com',
    client_secret='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',
    access_token_url='https://accounts.google.com/o/oauth2/token',
    access_token_params=None,
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    authorize_params={'access_type': 'offline', 'prompt': 'consent'},
    api_base_url='https://www.googleapis.com/oauth2/v1/',
    client_kwargs={'scope': 'email profile'},
)

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
from app.models import Sensor, Turbidez, Perfil, Usuario

from app.controllers import turbidez_controller, perfil_controller, usuario_controller, auth_controller

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
app.add_url_rule('/register', 'register', auth_controller.register, methods=['POST'])
app.add_url_rule('/login', 'login', auth_controller.login, methods=['POST'])
app.add_url_rule('/refresh', 'refresh_token', auth_controller.refresh_token, methods=['POST'])
app.add_url_rule('/reset-password', 'reset_password_request', auth_controller.reset_password_request, methods=['POST'])
app.add_url_rule('/login/google', 'login_google', auth_controller.login_google, methods=['GET'])
app.add_url_rule('/login/google/callback', 'authorize_google', auth_controller.authorize_google)


@app.route('/')
def home():
    return redirect(url_for('flasgger.apidocs'))

