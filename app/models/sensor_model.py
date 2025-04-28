from datetime import datetime
import uuid
from sqlalchemy.dialects.postgresql import UUID
from app import db

class Sensor(db.Model):
    __tablename__ = 'sensor'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    usuario_id = db.Column(UUID(as_uuid=True), db.ForeignKey('usuario.id'), nullable=False)
    propriedade_id = db.Column(UUID(as_uuid=True), db.ForeignKey('propriedade.id'), nullable=False)
    tanque_id = db.Column(UUID(as_uuid=True), db.ForeignKey('tanque.id'), nullable=False)
    nome = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relacionamentos
    usuario = db.relationship('Usuario', backref=db.backref('sensores', lazy=True))
    propriedade = db.relationship('Propriedade', backref=db.backref('sensores', lazy=True))
    tanque = db.relationship('Tanque')

    def to_dict(self):
        sensor_dict = {
            'id': self.id,
            'usuario_id': self.usuario_id,
            'propriedade_id': self.propriedade_id,
            'nome': self.nome,
            'created_at': self.created_at.strftime('%d/%m/%Y %H:%M:%S')
        }
        if self.tanque:
            sensor_dict['tanque_id'] = self.tanque_id
            sensor_dict['tanque_nome'] = self.tanque.nome
        return sensor_dict