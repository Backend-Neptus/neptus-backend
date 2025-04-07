from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from app.models.perfil_model import Perfil


class Usuario(db.Model):
  __tablename__ = 'usuario'

  id = db.Column(db.Integer, primary_key=True)
  nome = db.Column(db.String(100), nullable=False)
  email = db.Column(db.String(120), unique=True, nullable=False)
  senha_hash = db.Column(db.String(200), nullable=True)
  google_login = db.Column(db.Boolean, default=False)
  is_admin = db.Column(db.Boolean, default=False)
  is_active = db.Column(db.Boolean, default=True)

  perfil_id = db.Column(db.Integer, db.ForeignKey('perfil.id'), nullable=False)
  perfil = db.relationship('Perfil', back_populates='usuarios')

  def set_senha(self, senha):
    self.senha_hash = generate_password_hash(senha)

  def verificar_senha(self, senha):
    return check_password_hash(self.senha_hash, senha)
