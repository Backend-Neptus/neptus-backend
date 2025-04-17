from datetime import datetime
import uuid
from sqlalchemy.dialects.postgresql import UUID
from app import db

propriedade_usuarios = db.Table(
    'propriedade_usuarios',
    db.Column('propriedade_id',
              db.UUID(as_uuid=True),
              db.ForeignKey('propriedade.id'),
              primary_key=True),
    db.Column('usuario_id',
              db.UUID(as_uuid=True),
              db.ForeignKey('usuario.id'),
              primary_key=True))


class Propriedade(db.Model):
  __tablename__ = 'propriedade'
  id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
  nome = db.Column(db.String(50), unique=True, nullable=False)
  usuarios = db.relationship('Usuario',
                             secondary=propriedade_usuarios,
                             back_populates='propriedades')
  proprietario_id = db.Column(UUID(as_uuid=True), db.ForeignKey('usuario.id'))
  proprietario = db.relationship('Usuario', foreign_keys=[proprietario_id])
  created_at = db.Column(db.DateTime, default=datetime.utcnow)
  updated_at = db.Column(db.DateTime,
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
        'created_at': self.created_at.strftime('%d/%m/%Y %H:%M:%S'),
        'updated_at': self.updated_at.strftime('%d/%m/%Y %H:%M:%S')
    }
  def to_dict_my_propriedades(self, usuario_id):
    if self.proprietario_id != usuario_id:
        return {}  # Retorna um dicionário vazio se os IDs não coincidirem
    return {
        "proprietario_id": self.proprietario_id,
        "propriedade_nome": self.nome,
    }
