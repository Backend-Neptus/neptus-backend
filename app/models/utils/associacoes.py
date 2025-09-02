from sqlalchemy.dialects.postgresql import UUID
from app import db

propriedade_usuarios = db.Table(
    'propriedade_usuarios',
    db.Column('propriedade_id', db.UUID(as_uuid=True), db.ForeignKey('propriedade.id'), primary_key=True),
    db.Column('usuario_id', db.UUID(as_uuid=True), db.ForeignKey('usuario.id'), primary_key=True),
)