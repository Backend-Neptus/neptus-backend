from datetime import datetime, timezone
import uuid
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import validates
from app.models.utils.associacoes import propriedade_usuarios


class Usuario(db.Model):
  __tablename__ = 'usuario'

  id = db.Column(db.Uuid, primary_key=True, default=uuid.uuid4)
  nome = db.Column(db.String(100), nullable=False)
  email = db.Column(db.String(120), unique=True, nullable=False)
  senha = db.Column(db.String(200), nullable=False)
  e_admin = db.Column(db.Boolean, default=False)
  esta_ativo = db.Column(db.Boolean, default=True)

  perfil_id = db.Column(db.Uuid,
                        db.ForeignKey('perfil.id'),
                        nullable=False)
  perfil = db.relationship('Perfil', back_populates='usuarios', lazy='selectin')

  criado_em = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
  atualizado_em = db.Column(db.DateTime,
                         default=lambda: datetime.now(timezone.utc),
                         onupdate=lambda: datetime.now(timezone.utc))
  
  propriedades = db.relationship('Propriedade',
                                 secondary=propriedade_usuarios,
                                 back_populates='usuarios',
                                 overlaps="perfis",
                                 lazy='selectin')

  @validates('email')
  def validate_email(self, key, address):
    if address:
      return address.lower().strip()
    return address

  def set_senha(self, senha):
    self.senha = generate_password_hash(senha)

  def verificar_senha(self, senha):
    return check_password_hash(self.senha, senha)

  def to_dict(self, include_propriedades=True):
    data = {
        'id': str(self.id),
        'nome': self.nome,
        'email': self.email,
        'e_admin': self.e_admin, 
        'esta_ativo': self.esta_ativo,
        'perfil_id': str(self.perfil_id),
        'perfil_nome': self.perfil.nome if self.perfil else None,
        'total_propriedades': len(self.propriedades),
        'criado_em': self.criado_em.isoformat() if self.criado_em else None,
        'atualizado_em': self.atualizado_em.isoformat() if self.atualizado_em else None
    }
    
    if include_propriedades:
      data['propriedades'] = [
          {"nome": p.nome, "propriedade_id": str(p.id)} 
          for p in self.propriedades
      ]
      
    return data

  def usuarios_to_dict(self):
    return self.to_dict(include_propriedades=False)

