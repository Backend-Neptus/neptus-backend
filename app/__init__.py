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
from app.models import Perfil, Usuario, Propriedade, Tanque

# Importando as rotas
from app.routes import register_routes
register_routes(app)

@app.route('/')
def home():
    return redirect('https://docs.neptus.publicvm.com/share/zdm8lrpgbk/p/neptus-documentacao-BVR7NIppdg')

