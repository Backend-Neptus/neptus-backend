from datetime import datetime, timezone
import uuid
from app import db


class Perfil(db.Model):
  __tablename__ = 'perfil'
  id = db.Column(db.Uuid, primary_key=True, default=uuid.uuid4)
  nome = db.Column(db.String(50), unique=True, nullable=False)
  permissoes = db.Column(db.JSON, nullable=False, default=[])
  usuarios = db.relationship('Usuario', back_populates='perfil', lazy='selectin')
  criado_em = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
  atualizado_em = db.Column(db.DateTime,
                         default=lambda: datetime.now(timezone.utc),
                         onupdate=lambda: datetime.now(timezone.utc))

  def to_dict(self):
    return {
        "id": str(self.id),
        "nome": self.nome,
        "permissoes": self.permissoes,
        "usuarios_count": len(self.usuarios),
        "criado_em": self.criado_em.isoformat() if self.criado_em else None,
        "atualizado_em": self.atualizado_em.isoformat() if self.atualizado_em else None,
    }

