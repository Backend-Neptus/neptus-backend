from flask import request, jsonify
from app import db
from app.models.usuario_model import Usuario
from app.models.perfil_model import Perfil
from app.enum.PermissionEnum import PermissionEnum
from app.exceptions import (BadRequestError, ConflictRequestError,
                            UserDisabledError, GoogleLoginRequestError,
                            NotFoundRequestError, InvalidCredentialsError)


class UsuarioService():

  def registrar_usuario(nome: str, email: str, senha: str, perfil_id: str):

    if (not nome) or (not email) or (not senha) or (not perfil_id):
      raise BadRequestError(
          "Os campos 'nome', 'email', 'senha' e 'perfil_id' devem ser preenchidos"
      )

    if Usuario.query.filter_by(email=email).first():
      raise ConflictRequestError("E-mail ja cadastrado")

    perfil = Perfil.query.get(perfil_id)
    if not perfil:
      raise NotFoundRequestError("Perfil nao encontrado")

    usuario = Usuario(nome=nome, email=email, perfil_id=perfil.id)
    usuario.set_senha(senha)
    db.session.add(usuario)
    db.session.commit()

    return usuario

  def listar_usuarios():
    return [{
        'id': usuario.id,
        'nome': usuario.nome,
        'email': usuario.email,
        'perfil_id': usuario.perfil_id,
        'perfil_nome': usuario.perfil.nome,
        'is_admin': usuario.is_admin,
        'is_active': usuario.is_active,
        'google_login': usuario.google_login,
        'created_at': usuario.updated_at.strftime('%d/%m/%Y %H:%M:%S'),
        'updated_at': usuario.updated_at.strftime('%d/%m/%Y %H:%M:%S')
    } for usuario in Usuario.query.order_by(Usuario.created_at).all()]

  def atualizar_usuario(id: str, nome: str, email: str, perfil_id: str):
    if (not nome) or (not email) or (not perfil_id):
      raise BadRequestError(
          "Os campos 'nome', 'email' e 'perfil_id' devem ser preenchidos")
    usuario = Usuario.query.get(id)

    if not usuario:
      raise NotFoundRequestError("Usuário não encontrado")

    perfil = Perfil.query.get(perfil_id)
    if not perfil:
      raise NotFoundRequestError("Perfil nao encontrado")

    if usuario.email != email:
      usuario_email = Usuario.query.filter_by(email=email).first()
      if usuario_email and usuario_email.id != usuario.id:
        raise ConflictRequestError("E-mail ja cadastrado")

    usuario.nome = nome
    usuario.email = email
    usuario.perfil_id = perfil_id
    db.session.commit()

    return usuario

  def status_usuario(id: str, status: bool):
    usuario = Usuario.query.get(id)

    if not usuario:
      raise NotFoundRequestError("Usuário nao encontrado")

    if status:
      usuario.is_active = True
    else:
      usuario.is_active = False

    db.session.commit()
    return usuario

  def buscar_usuario(id):
    usuario = Usuario.query.get(id)
    if not usuario:
      raise NotFoundRequestError("Usuário nao encontrado")
    return usuario
