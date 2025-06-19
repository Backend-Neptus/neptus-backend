from app import db
from sqlalchemy.dialects.postgresql import UUID

class Turbidez(db.Model):
    __tablename__ = 'turbidez'
    id = db.Column(db.Integer, primary_key=True)
    valor = db.Column(db.String, nullable=False)
    proprietario_id = db.Column(UUID(as_uuid=True), db.ForeignKey('usuario.id'))
    usuario_id = db.Column(UUID(as_uuid=True),
                        db.ForeignKey('usuario.id'),
                        nullable=False)

    def __repr__(self):
        return f"<Turbidez {self.id}, {self.valor}>"