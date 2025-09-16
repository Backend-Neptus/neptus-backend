from datetime import datetime
import uuid
from sqlalchemy.dialects.postgresql import UUID
from app import db
from sqlalchemy.dialects.postgresql import ARRAY


class Perfil(db.Model):
  __tablename__ = 'perfil'
  id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
  nome = db.Column(db.String(50), unique=False, nullable=False)
  permissoes = db.Column(ARRAY(db.String), nullable=False, default=[])
  usuarios = db.relationship('Usuario', back_populates='perfil')
  created_at = db.Column(db.DateTime, default=datetime.utcnow)
  updated_at = db.Column(db.DateTime,
                         default=datetime.utcnow,
                         onupdate=datetime.utcnow)

  def to_dict(self):
    return {
        "id": self.id,
        "nome": self.nome,
        "permissoes": self.permissoes,
        "usuarios": len(self.usuarios),
        "criado_em": self.created_at.strftime('%d/%m/%Y %H:%M:%S'),
        "atualizado_em": self.updated_at.strftime('%d/%m/%Y %H:%M:%S'),
    }
