from datetime import timedelta
from app import db
from app.models.usuario_model import Usuario
from flask_jwt_extended import create_access_token, create_refresh_token

def create_token(id: str, nome: str, isAdmin: bool, permissoes: list, perfil: str, email: str ):
    acesss_token = create_access_token(identity=str(id), additional_claims={"nome": nome, "email":email, "isAdmin": isAdmin,"perfil": perfil, "permissoes": permissoes }, expires_delta=timedelta(hours=24))
    return  acesss_token
    
def refresh_token(id: str):
    refresh_token = create_refresh_token(identity=str(id), expires_delta=timedelta(days=7))
    return refresh_token