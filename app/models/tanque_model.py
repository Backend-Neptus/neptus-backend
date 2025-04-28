from datetime import datetime
import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey
from app import db

class Tanque(db.Model):
    __tablename__ = 'tanque'
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nome = db.Column(db.String(50), nullable=False)
    propriedade_id = db.Column(UUID(as_uuid=True), ForeignKey('propriedade.id'), nullable=False)
    usuario_id = db.Column(UUID(as_uuid=True), ForeignKey('usuario.id'), nullable=False)
    status = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relacionamentos
    propriedade = relationship('Propriedade', backref=db.backref('tanques', lazy=True))
    usuario = relationship('Usuario', back_populates='tanques')
    sensores = relationship('Sensor', foreign_keys='[Sensor.tanque_id]', backref='sensores_no_tanque')

    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'propriedade_id': self.propriedade_id,
            'propriedade_nome': self.propriedade.nome if self.propriedade else None,
            'status': self.status,
            'usuario_nome': self.usuario.nome if self.usuario else None,
            'usuario_id': self.usuario.id if self.usuario else None,
            'created_at': self.created_at.strftime('%d/%m/%Y %H:%M:%S'),
            'updated_at': self.updated_at.strftime('%d/%m/%Y %H:%M:%S'),
        }