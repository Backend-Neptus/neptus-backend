from app import db
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
import uuid

class Sensor(db.Model):
  __tablename__ = 'sensor'
  id = db.Column(db.Integer, primary_key=True)
  nome = db.Column(db.String, nullable=False)
  turbidez_id = db.Column(UUID(as_uuid=True), db.ForeignKey('turbo.id'), nullable=False, unique=True)
  created_at = db.Column(db.DateTime,default=datetime.utcnow)
  updated_at = db.Column(db.DateTime,
                         default=datetime.utcnow)


  def __repr__(self):
    return f"<Sensor {self.id}, {self.nome}>"
  
  def to_dict(self):
    return {
        'id': self.id,
        'nome': self.nome,
        'turbidez_id': str(self.turbidez_id),
        'usuario_id': str(self.turbidez.usuario_id),
        'proprietario_id': str(self.turbidez.proprietario_id),
        'created_at': self.created_at.strftime('%d/%m/%Y %H:%M:%S'),
        'updated_at': self.updated_at.strftime('%d/%m/%Y %H:%M:%S')
    }
