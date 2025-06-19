from app import db
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
import uuid

class Sensor(db.Model):
  __tablename__ = 'sensor'
  id = db.Column(db.Integer, primary_key=True)
  nome = db.Column(db.String, nullable=False)
  usuario_id = db.Column(UUID(as_uuid=True), db.ForeignKey('usuario.id'), nullable=False, unique=True)
  propriedade_id = db.Column(UUID(as_uuid=True), db.ForeignKey('propriedade.id'), nullable=False, unique=True)
  created_at = db.Column(db.DateTime,default=datetime.utcnow)
  updated_at = db.Column(db.DateTime,
                         default=datetime.utcnow,
                         onupdate=datetime.utcnow)

  def __repr__(self):
    return f"<Sensor {self.id}, {self.nome}>"
  
  def to_dict(self):
    return {
        'id': self.id,
        'nome': self.nome,
        'usuario_id': str(self.usuario_id),
        'propriedade_id': str(self.propriedade_id),
        'created_at': self.created_at.strftime('%d/%m/%Y %H:%M:%S'),
        'updated_at': self.updated_at.strftime('%d/%m/%Y %H:%M:%S')
    }
