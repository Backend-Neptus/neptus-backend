from app.enum.PermissionEnum import PermissionEnum
from app.exceptions import (BadRequestError, ConflictRequestError,
                            UserDisabledError, GoogleLoginRequestError,
                            NotFoundRequestError, InvalidCredentialsError)
from app import db
from app.models.propriedade_model import Propriedade
from app.models.usuario_model import Usuario
from flask import g


class PropriedadeService:

  def cadastrar_propriedade(self, nome: str, proprietario_id: str):
    if (not nome) or (not proprietario_id):
      raise BadRequestError(
          "Os campos 'nome' e 'proprietario_id' devem ser preenchidos")
    propriedade = Propriedade.query.filter_by(nome=nome).first()
    if propriedade:
      raise ConflictRequestError("Propriedade com mesmo nome ja cadastrada")
    usuario = Usuario.query.get(proprietario_id)
    print(proprietario_id)
    print(usuario)
    if not usuario:
      raise NotFoundRequestError("Proprietario nao encontrado")

    propriedade = Propriedade()
    propriedade.nome = nome
    propriedade.proprietario_id = proprietario_id
    propriedade.usuarios.append(usuario)
    db.session.add(propriedade)
    db.session.commit()
    return propriedade

  def listar_propriedades(self):
    return [
        propriedade.to_dict() for propriedade in Propriedade.query.order_by(
            Propriedade.created_at).all()
    ]

  def atualizar_propriedade(self, id: str, nome: str, proprietario_id: str):
    if (not nome) or (not proprietario_id):
      raise BadRequestError(
          "Os campos 'nome' e 'proprietario_id' devem ser preenchidos")
    propriedade = self.__propriedade_existe(id)
    nome_existente = Propriedade.query.filter_by(nome=nome).first()
    if propriedade.id != nome_existente.id:
      raise ConflictRequestError("Propriedade com mesmo nome ja cadastrada")

    if propriedade.proprietario_id != proprietario_id:
      novo_usuario = Usuario.query.get(proprietario_id)
      if not novo_usuario:
        raise NotFoundRequestError("Proprietário não encontrado")

      if novo_usuario not in propriedade.usuarios:
        propriedade.usuarios.append(novo_usuario)

      usuario_antigo = Usuario.query.get(propriedade.proprietario_id)
      if usuario_antigo and usuario_antigo in propriedade.usuarios:
        propriedade.usuarios.remove(usuario_antigo)

      propriedade.proprietario_id = proprietario_id

    propriedade.nome = nome
    db.session.commit()
    return propriedade

  def detalhar_propriedade(self, id: str):
    propriedade = Propriedade.query.get(id)
    if not propriedade:
      raise NotFoundRequestError("Propriedade nao encontrada")
    return propriedade

  def adicionar_usuario(self, id: str, usuario_id: str):
    propriedade = self.__propriedade_existe(id)
    usuario = self.__usuario_existe(usuario_id)
    if usuario in propriedade.usuarios:
      raise ConflictRequestError("Usuário ja cadastrado na propriedade")
    print(self.__verificar_permissao_propriedade(propriedade))
    if self.__verificar_permissao_propriedade(propriedade):
      propriedade.usuarios.append(usuario)
      db.session.commit()
    else:
      raise BadRequestError(
          "Usuário nao possui permissao para adicionar usuario a propriedade")
    return propriedade

  def remover_usuario(self, id: str, usuario_id: str):
    propriedade = self.__propriedade_existe(id)
    usuario = self.__usuario_existe(usuario_id)
    if usuario not in propriedade.usuarios:
      raise ConflictRequestError("Usuário nao cadastrado na propriedade")
    print(self.__verificar_permissao_propriedade(propriedade))
    if self.__verificar_permissao_propriedade(propriedade):
      propriedade.usuarios.remove(usuario)
      db.session.commit()
    else:
      raise BadRequestError(
          "Usuário nao possui permissao para adicionar usuario a propriedade")
    return propriedade

  def __usuario_existe(self, usuario_id):
    usuario = Usuario.query.get(usuario_id)
    if not usuario:
      raise NotFoundRequestError("Usuário nao encontrado")
    return usuario

  def __verificar_permissao_propriedade(self, propriedade):
    usuario_request = g.usuario
    return (usuario_request.is_admin) or (
        usuario_request
        is propriedade.proprietario) or (PermissionEnum.PERFIL_CRIAR.value
                                         in usuario_request.perfil.permissoes)

  def __propriedade_existe(self, id):
    propriedade = Propriedade.query.get(id)
    if not propriedade:
      raise NotFoundRequestError("Propriedade nao encontrada")
    return propriedade
