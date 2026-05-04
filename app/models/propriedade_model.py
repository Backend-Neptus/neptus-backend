from datetime import datetime, timezone
import uuid
from app import db
from app.models.utils.associacoes import propriedade_usuarios

class Propriedade(db.Model):
  __tablename__ = 'propriedade'
  id = db.Column(db.Uuid, primary_key=True, default=uuid.uuid4)
  nome = db.Column(db.String(50), unique=True, nullable=False)
  usuarios = db.relationship('Usuario',
                             secondary=propriedade_usuarios,
                             back_populates='propriedades',
                             overlaps="propriedades,perfis",
                             lazy='selectin')
  proprietario_id = db.Column(db.Uuid, db.ForeignKey('usuario.id'))
  proprietario = db.relationship('Usuario', foreign_keys=[proprietario_id], lazy='selectin')
  criado_em = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
  atualizado_em = db.Column(db.DateTime,
                         default=lambda: datetime.now(timezone.utc),
                         onupdate=lambda: datetime.now(timezone.utc))

  def to_dict(self, include_usuarios=True):
    data = {
        'id': str(self.id),
        'nome': self.nome,
        'proprietario_id': str(self.proprietario_id) if self.proprietario_id else None,
        'proprietario_nome': self.proprietario.nome if self.proprietario else None,
        'total_usuarios': len(self.usuarios),
        'criado_em': self.criado_em.isoformat() if self.criado_em else None,
        'atualizado_em': self.atualizado_em.isoformat() if self.atualizado_em else None
    }
    
    if include_usuarios:
      data['usuarios'] = [usuario.usuarios_to_dict() for usuario in self.usuarios]
      
    return data

  def propriedades_to_dict(self):
    return self.to_dict(include_usuarios=False)