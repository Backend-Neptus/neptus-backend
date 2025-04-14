from datetime import datetime
import uuid
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.dialects.postgresql import UUID


class Usuario(db.Model):
  __tablename__ = 'usuario'

  id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
  nome = db.Column(db.String(100), nullable=False)
  email = db.Column(db.String(120), unique=True, nullable=False)
  senha_hash = db.Column(db.String(200), nullable=True)
  google_login = db.Column(db.Boolean, default=False)
  is_admin = db.Column(db.Boolean, default=False)
  is_active = db.Column(db.Boolean, default=True)

  perfil_id = db.Column(UUID(as_uuid=True), db.ForeignKey('perfil.id'), nullable=False)
  perfil = db.relationship('Perfil', back_populates='usuarios')

  created_at = db.Column(db.DateTime, default=datetime.utcnow)
  updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

  def set_senha(self, senha):
    self.senha_hash = generate_password_hash(senha)

  def verificar_senha(self, senha):
    return check_password_hash(self.senha_hash, senha)

  def to_dict(self):
    return {
        'id': self.id,
        'nome': self.nome,
        'email': self.email,
        'google_login': self.google_login,
        'is_admin': self.is_admin,
        'is_active': self.is_active,
        'perfil_id': self.perfil_id,
        'created_at': self.created_at.strftime('%d/%m/%Y %H:%M:%S'),
        'updated_at': self.updated_at.strftime('%d/%m/%Y %H:%M:%S')
    }