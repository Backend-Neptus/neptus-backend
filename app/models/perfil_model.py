from app import db
from app.enum.PermissionEnum import PermissionEnum
from sqlalchemy.dialects.postgresql import ARRAY

class Perfil(db.Model):
    __tablename__ = 'perfil'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), unique=True, nullable=False)
    permissoes = db.Column(ARRAY(db.String), nullable=False, default=[])

