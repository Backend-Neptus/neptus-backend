from datetime import datetime
import uuid
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.dialects.postgresql import UUID
from app.models.propriedade_model import propriedade_usuarios


class Usuario(db.Model):
  __tablename__ = 'usuario'

  id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
  nome = db.Column(db.String(100), nullable=False)
  email = db.Column(db.String(120), unique=True, nullable=False)
  senha = db.Column(db.String(200), nullable=True)
  e_admin = db.Column(db.Boolean, default=False)
  esta_ativo = db.Column(db.Boolean, default=True)

  perfil_id = db.Column(UUID(as_uuid=True),
                        db.ForeignKey('perfil.id'),
                        nullable=False)
  perfil = db.relationship('Perfil', back_populates='usuarios')

  criado_em = db.Column(db.DateTime, default=datetime.utcnow)
  atualizado_em = db.Column(db.DateTime,
                         default=datetime.utcnow,
                         onupdate=datetime.utcnow)
  propriedades = db.relationship('Propriedade',
                                 secondary=propriedade_usuarios,
                                 back_populates='usuarios',
                                 overlaps="perfis")

  def set_senha(self, senha):
    self.senha = generate_password_hash(senha)

  def verificar_senha(self, senha):
    return check_password_hash(self.senha, senha)

  def to_dict(self):
    return {
        'id':
        self.id,
        'nome':
        self.nome,
        'email':
        self.email,
        'e_admin':
        self.e_admin, 
        'esta_ativo':
        self.esta_ativo,
        'perfil_id':
        self.perfil_id,
        'perfil_nome': self.perfil.nome if self.perfil else None,
        'total_propriedades':
        len(self.propriedades),
        'propriedades':
        [{"nome": propriedade.nome, "propriedade_id": propriedade.id} for propriedade in self.propriedades],
        'criado_em':
        self.criado_em.strftime('%d/%m/%Y %H:%M:%S'),
        'atualizado_em':
        self.atualizado_em.strftime('%d/%m/%Y %H:%M:%S')
    }

  def usuarios_to_dict(self):
    return {
        'id': self.id,
        'nome': self.nome,
        'email': self.email,
        'e_admin': self.e_admin,
        'esta_ativo': self.esta_ativo,
        'perfil_id': self.perfil_id,
        'perfil_nome': self.perfil.nome if self.perfil else None,
        'total_propriedades': len(self.propriedades),
        'criado_em': self.criado_em.strftime('%d/%m/%Y %H:%M:%S'),
        'atualizado_em': self.atualizado_em.strftime('%d/%m/%Y %H:%M:%S')
    }
