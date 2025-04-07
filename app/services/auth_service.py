from flask import request, jsonify, url_for
from flask_jwt_extended import create_access_token
from app import db, google
from app.exceptions import (BadRequestError, ConflictRequestError,
                            UserDisabledError, GoogleLoginRequestError,
                            NotFoundRequestError, InvalidCredentialsError)
from app.models.usuario_model import Usuario
from app.utils import default_perfil, reset_password


class AuthService:

  def registrar_usuario(self, nome: str, email: str, senha: str):

    if (not nome) or (not email) or (not senha):
      raise BadRequestError(
          "Os campos 'nome', 'email' e 'senha' devem ser preenchidos")

    if Usuario.query.filter_by(email=email).first():
      raise ConflictRequestError("E-mail ja cadastrado")

    perfil = default_perfil.get_default_perfil()
    usuario = Usuario(nome=nome, email=email, perfil_id=perfil.id)
    usuario.set_senha(senha)
    db.session.add(usuario)
    db.session.commit()

    return jsonify({"mensagem": "Usuário cadastrado com sucesso!"}), 201

  def login(self, email: str, senha: str):
    usuario = Usuario.query.filter_by(email=email).first()

    if not usuario:
      raise NotFoundRequestError("Usuário não cadastrado")

    if not usuario.is_active:
      raise UserDisabledError("Usuário desativado")

    if usuario.google_login:
      raise GoogleLoginRequestError(
          "Usuário cadastrado via Google, use o login com Google")

    if not usuario.verificar_senha(senha):
      raise InvalidCredentialsError("Email ou senha inválidos")

    return create_access_token(identity=str(usuario.id))

  def authorize_google(self, nome: str, email: str):
    usuario = Usuario.query.filter_by(email=email).first()

    if not usuario:
      perfil = default_perfil.get_default_perfil()
      usuario = Usuario(nome=nome,
                        email=email,
                        perfil_id=perfil.id,
                        google_login=True)
      db.session.add(usuario)
      db.session.commit()

    if not usuario.is_active:
      raise UserDisabledError("Usuário desativado")

    if not usuario.google_login:
      raise GoogleLoginRequestError("Usuário não cadastrado via Google")

    return create_access_token(identity=str(usuario.id))

  def recuperar_senha(self, email):
    usuario = Usuario.query.filter_by(email=email).first()

    if not usuario:
      raise NotFoundRequestError("E-mail não encontrado")

    if not usuario.is_active:
      raise UserDisabledError("Usuário desativado")

    if usuario.google_login:
      raise GoogleLoginRequestError("Usuário cadastrado via Google")

    nova_senha = reset_password.gerar_nova_senha()
    usuario.set_senha(nova_senha)
    db.session.commit()

    reset_password.enviar_senha(email, nova_senha, usuario.nome)
    return "Nova senha enviada para o e-mail"
