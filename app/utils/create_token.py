from datetime import timedelta
from app import db
from app.models.usuario_model import Usuario
from flask_jwt_extended import create_access_token, create_refresh_token

def create_token(id: str, nome: str):
    acesss_token = create_access_token(identity=str(id), additional_claims={"nome": nome}, expires_delta=timedelta(hours=1))
    return  acesss_token
    
def refresh_token(id: str):
    refresh_token = create_refresh_token(identity=str(id), expires_delta=timedelta(days=30))
    return refresh_token