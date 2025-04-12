import uuid
from sqlalchemy.dialects.postgresql import UUID
from app import db
from sqlalchemy.dialects.postgresql import ARRAY


class Perfil(db.Model):
  __tablename__ = 'perfil'
  id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
  nome = db.Column(db.String(50), unique=True, nullable=False)
  permissoes = db.Column(ARRAY(db.String), nullable=False, default=[])
  usuarios = db.relationship('Usuario', back_populates='perfil')

  def to_dict(self):
    return {"id": self.id, "nome": self.nome, "permissoes": self.permissoes}
