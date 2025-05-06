from sqlalchemy.dialects.postgresql import UUID
from app import db

propriedade_usuarios = db.Table(
    'propriedade_usuarios',
    db.Column('propriedade_id', db.UUID(as_uuid=True), db.ForeignKey('propriedade.id'), primary_key=True),
    db.Column('usuario_id', db.UUID(as_uuid=True), db.ForeignKey('usuario.id'), primary_key=True),
    db.Column('perfil_local', UUID(as_uuid=True), db.ForeignKey('perfil.id'), nullable=True)
)

propriedade_perfil = db.Table(
    'propriedade_perfil',
    db.Column('propriedade_id', db.UUID(as_uuid=True), db.ForeignKey('propriedade.id'), primary_key=True),
    db.Column('perfil_id', db.UUID(as_uuid=True), db.ForeignKey('perfil.id'), primary_key=True)
)