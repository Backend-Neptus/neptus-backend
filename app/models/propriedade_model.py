from datetime import datetime
import uuid
from sqlalchemy.dialects.postgresql import UUID
from app import db
from app.models.utils.associacoes import propriedade_usuarios

class Propriedade(db.Model):
  __tablename__ = 'propriedade'
  id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
  nome = db.Column(db.String(50), unique=True, nullable=False)
  usuarios = db.relationship('Usuario',
                             secondary=propriedade_usuarios,
                             back_populates='propriedades',
                             overlaps="propriedades,perfis")
  proprietario_id = db.Column(UUID(as_uuid=True), db.ForeignKey('usuario.id'))
  proprietario = db.relationship('Usuario', foreign_keys=[proprietario_id])
  criado_em = db.Column(db.DateTime, default=datetime.utcnow)
  atualizado_em = db.Column(db.DateTime,
                         default=datetime.utcnow,
                         onupdate=datetime.utcnow)

  def to_dict(self):
    return {
        'id': self.id,
        'nome': self.nome,
        'total_usuarios': len(self.usuarios),
        'usuarios': [usuario.usuarios_to_dict() for usuario in self.usuarios],
        'proprietario_id': self.proprietario_id,
        'proprietario_nome': self.proprietario.nome,
        'criado_em': self.criado_em.strftime('%d/%m/%Y %H:%M:%S'),
        'atualizado_em': self.atualizado_em.strftime('%d/%m/%Y %H:%M:%S')
    }

  def propriedades_to_dict(self):
    return {
        'id': self.id,
        'nome': self.nome,
        'total_usuarios': len(self.usuarios),
        'proprietario_id': self.proprietario_id,
        'proprietario_nome': self.proprietario.nome,
        'criado_em': self.criado_em.strftime('%d/%m/%Y %H:%M:%S'),
        'atualizado_em': self.atualizado_em.strftime('%d/%m/%Y %H:%M:%S')
    }