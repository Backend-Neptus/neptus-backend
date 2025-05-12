from itsdangerous import URLSafeTimedSerializer
from app.enum.PermissionEnum import PermissionEnum
from app.exceptions import (BadRequestError, ConflictRequestError,
                            NotFoundRequestError)
from app import db
from app.models.perfil_model import Perfil
from app.models.propriedade_model import Propriedade
from app.models.usuario_model import Usuario
from flask import g
from app.config.app_config import APP_CONFIG

from app.utils import convidar_usuario
from app.utils.permissoes_perfil_local import PermissaoPerfilLocal


class PropriedadeService:

  def cadastrar_propriedade(self, nome: str, proprietario_id: str):
    self.__verificar_dados(nome, proprietario_id)
    propriedade = Propriedade.query.filter_by(nome=nome).first()
    if propriedade:
      raise ConflictRequestError("Propriedade com mesmo nome já cadastrada")
    usuario = Usuario.query.get(proprietario_id)
    print(proprietario_id)
    print(usuario)
    if not usuario:
      raise NotFoundRequestError("Usuário não encontrado")

    propriedade = Propriedade()
    propriedade.nome = nome
    propriedade.proprietario_id = proprietario_id
    propriedade.usuarios.append(usuario)
    db.session.add(propriedade)
    db.session.commit()
    return propriedade

  def listar_propriedades(self, page, per_page):
    if per_page > 50:
      per_page = 50
    propriedade = Propriedade.query.order_by(Propriedade.created_at).paginate(
        page=page, per_page=per_page, error_out=False)
    return {
        'total': propriedade.total,
        'pagina_atual': propriedade.page,
        'itens_por_pagina': propriedade.per_page,
        'total_paginas': propriedade.pages,
        'propriedades': [propriedade.to_dict() for propriedade in propriedade]
    }

  def atualizar_propriedade(self, id: str, nome: str, proprietario_id: str):
    if (not nome) or (not proprietario_id):
        raise BadRequestError("Os campos 'nome' e 'proprietario_id' devem ser preenchidos")

    propriedade = self.__propriedade_existe(id)

    nome_existente = Propriedade.query.filter_by(nome=nome).first()
    if nome_existente and nome_existente.id != propriedade.id:
        raise ConflictRequestError("Propriedade com mesmo nome já cadastrada")

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
      raise NotFoundRequestError("Propriedade não encontrada")
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
          "Usuário nao possui permissao para remover usuario a propriedade")
    return propriedade

  def convidar_usuario(self, id: str, email: str):
    propriedade = self.__propriedade_existe(id)
    if self.__verificar_permissao_propriedade(propriedade):
      usuario = Usuario.query.filter_by(email=email).first()
      if not usuario:
        raise NotFoundRequestError(
            "Usuário não cadastrado no sistema, efetue o cadastro primeiro")
      if usuario in propriedade.usuarios:
        raise ConflictRequestError("Usuário ja cadastrado na propriedade")
      s = URLSafeTimedSerializer(APP_CONFIG.CONVITE_TOKEN_SECRET)
      token_convite = s.dumps((email, str(propriedade.id)),
                              salt=APP_CONFIG.CONVITE_TOKEN_SALT)
      usuario_request = g.usuario
      convidar_usuario.enviar_convite(email_destino=email,
                                      token_convite=token_convite,
                                      nome_propriedade=propriedade.nome,
                                      usuario_request=usuario_request.nome,
                                      nome=usuario.nome)
    else:
      raise BadRequestError(
          "Voçe não possui permissão para convidar usuario a propriedade")
    return "Convite enviado com sucesso!"

  def convite_aceito(self, token_convite: str):
    s = URLSafeTimedSerializer(APP_CONFIG.CONVITE_TOKEN_SECRET)
    email, propriedade_id = s.loads(token_convite,
                                    salt=APP_CONFIG.CONVITE_TOKEN_SALT,
                                    max_age=3600)
    propriedade = self.__propriedade_existe(propriedade_id)
    usuario = Usuario.query.filter_by(email=email).first()
    if usuario in propriedade.usuarios:
      raise ConflictRequestError("Usuário ja cadastrado na propriedade")
    propriedade.usuarios.append(usuario)
    db.session.commit()
    return propriedade

  # COMO ISSO FUNCIONA?
  #TODO PRECISA FAZER VALIDACOES DE CAMPOS E PERMISSOES
  def salvar_perfil_local(nome, permissoes, propriedade_id):

    if not nome:
      raise BadRequestError("O campo 'nome' é obrigatório", data=nome)

    if not permissoes:
      raise BadRequestError("O campo 'permissoes' é obrigatório",
                            data={'permissoes': permissoes_invalidas})
    permissoes = [p.lower() for p in permissoes]
    permissoes = list(set(permissoes))
    permissoes_validas = {perm.value for perm in PermissionEnum}
    permissoes_invalidas = [
        p for p in permissoes if p not in permissoes_validas
    ]

    if permissoes_invalidas:
      raise BadRequestError(message="Permissões inválidas",
                            data={'permissoes': permissoes_invalidas})
    if PermissaoPerfilLocal().verificar_permissao_perfil_local(
        permissao=PermissionEnum.ATRIBUIR_PERFIL,
        propriedade_id=propriedade_id):
      propriedade = Propriedade.query.filter_by(id=propriedade_id).first()
      
      if not propriedade:
        raise NotFoundRequestError("Propriedade nao encontrada")
      
      perfil = Perfil(nome=nome, permissoes=permissoes)
      propriedade.perfis.append(perfil)
      db.session.add(perfil)
      db.session.commit()
    return perfil

  def autalizar_perfil_local_usuario(self, propriedade_id, perfil_id,
                                     usuario_id):
    propriedade = self.__propriedade_existe(
        propriedade_id
    )  #TEMOS UMA DUPLICAÇÃO DE PROPRIEDADE AQUI E EM VERIFICAR_PERMISSAO_PERFIL_LOCAL
    #TODO VERIFICAR SE ESSA DUPLICAÇÃO EH NECESSÁRIA
    perfil = Perfil.query.get(perfil_id)
    if perfil in propriedade.perfis:
      if PermissaoPerfilLocal().verificar_permissao_perfil_local(
          permissao=PermissionEnum.ATRIBUIR_PERFIL,
          propriedade_id=propriedade_id):
        usuario = self.__usuario_existe(usuario_id)
        PermissaoPerfilLocal().atualizar_perfil_local(
            usuario_id=usuario.id,
            propriedade_id=propriedade.id,
            novo_perfil_id=perfil.id)
        return f"Perfil do usuario {usuario.nome} atualizado com sucesso na propriedade {propriedade.nome}!"
    else:
      raise BadRequestError("Perfil nao cadastrado na propriedade")

  # ------------------
  # METODOS AUXILIARES
  # ------------------

  def __verificar_dados(self, nome, proprietario_id):
    if (not nome) or (not proprietario_id):
      raise BadRequestError(
          "Os campos 'nome' e 'proprietario_id' devem ser preenchidos")

  def __usuario_existe(self, usuario_id):
    usuario = Usuario.query.get(usuario_id)
    if not usuario:
      raise NotFoundRequestError("Usuário nao encontrado")
    return usuario

  def __verificar_permissao_propriedade(self, propriedade):
    usuario_request = g.usuario
    return (usuario_request.is_admin) or (usuario_request
                                          is propriedade.proprietario)

  def __propriedade_existe(self, id):
    propriedade = Propriedade.query.get(id)
    if not propriedade:
      raise NotFoundRequestError("Propriedade nao encontrada")
    return propriedade
