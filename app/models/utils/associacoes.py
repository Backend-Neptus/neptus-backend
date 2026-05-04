from app import db

propriedade_usuarios = db.Table(
    'propriedade_usuarios',
    db.Column('propriedade_id', db.Uuid, db.ForeignKey('propriedade.id'), primary_key=True),
    db.Column('usuario_id', db.Uuid, db.ForeignKey('usuario.id'), primary_key=True),
)