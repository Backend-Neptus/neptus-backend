import datetime
from io import BytesIO
import os
from sqlalchemy import text
from app import db
from app.models.usuario_model import Usuario
from app.models.perfil_model import Perfil
from app.exceptions import (BadRequestError, ConflictRequestError,
                            NotFoundRequestError)
from app.utils import default_perfil


class UsuarioService():

  def registrar_usuario(nome: str, email: str, senha: str, perfil_id: str):

    if (not nome) or (not email) or (not senha):
      raise BadRequestError(
          "Os campos 'nome', 'email' e 'senha' devem ser preenchidos"
      )
    if Usuario.query.filter_by(email=email).first():
      raise ConflictRequestError("E-mail já cadastrado")
    
    usuario = Usuario(nome=nome, email=email)
    if perfil_id:
        perfil = Perfil.query.get(perfil_id)
        if not perfil:
            raise NotFoundRequestError("Perfil não encontrado")
        else:
            usuario.perfil_id = perfil_id
    else:
        usuario.perfil_id = default_perfil.get_default_perfil().id

    usuario.set_senha(senha)
    db.session.add(usuario)
    db.session.commit()

    return usuario

  def listar_usuarios(page: int, per_page: int):
    if per_page > 50:
      per_page = 50

    usuario = Usuario.query.order_by(Usuario.criado_em).paginate(page=page,
                                     per_page=per_page,
                                     error_out=False)
    return {
        'total': usuario.total,
        'pagina_atual': usuario.page,
        'itens_por_pagina': usuario.per_page,
        'total_paginas': usuario.pages,
        'usuarios': [usuario.usuarios_to_dict() for usuario in usuario]
    }

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
    if status is None or status == '':
      raise BadRequestError("O campo 'status' deve ser preenchido")
    usuario = Usuario.query.get(id)
    if not usuario:
      raise NotFoundRequestError("Usuário nao encontrado")

    if status:
      usuario.esta_ativo = True
    else:
      usuario.esta_ativo = False

    db.session.commit()
    return usuario.usuarios_to_dict()

  def buscar_usuario(id):
    usuario = Usuario.query.get(id)
    if not usuario:
      raise NotFoundRequestError("Usuário nao encontrado")
    return usuario


  def relatorio_usuarios():
    resultado = db.session.execute(
        text(""" 
        SELECT 
            u.id,
            u.nome,
            u.email,
            u.e_admin,
            u.esta_ativo,
            u.perfil_id,
            to_char(u.criado_em, 'DD/MM/YYYY HH24:MI:SS') AS criado_em,
            to_char(u.atualizado_em, 'DD/MM/YYYY HH24:MI:SS') AS atualizado_em
        FROM usuario u
        LEFT JOIN propriedade_usuarios up ON up.usuario_id = u.id
        LEFT JOIN propriedade p ON p.id = up.propriedade_id
        ORDER BY u.criado_em;
    """))

    # Converter cada Row para dict usando _mapping
    usuarios = [dict(row._mapping) for row in resultado.fetchall()]

    return usuarios
    #TODO - implementar geração de PDF ou Excel conforme necessário