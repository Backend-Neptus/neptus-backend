from app.exceptions import (BadRequestError, ConflictRequestError,
                            NotFoundRequestError)
from app import db
from app.models.perfil_model import Perfil
from app.models.propriedade_model import Propriedade
from app.models.usuario_model import Usuario

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
    propriedade = Propriedade.query.order_by(Propriedade.criado_em).paginate(
        page=page, per_page=per_page, error_out=False)
    return {
        'total': propriedade.total,
        'pagina_atual': propriedade.page,
        'itens_por_pagina': propriedade.per_page,
        'total_paginas': propriedade.pages,
        'propriedades': [propriedade.propriedades_to_dict() for propriedade in propriedade]
    }

  def atualizar_propriedade(self, id: str, nome: str, proprietario_id):
    if (not nome) or (not proprietario_id):
        raise BadRequestError("Os campos 'nome' e 'proprietario_id' devem ser preenchidos")

    propriedade = self.__propriedade_existe(id)

    nome_existente = Propriedade.query.filter_by(nome=nome).first()
    if nome_existente and nome_existente.id != propriedade.id:
        raise ConflictRequestError("Propriedade com mesmo nome já cadastrada")

    usuario = Usuario.query.get(proprietario_id)
    if not usuario:
        raise NotFoundRequestError("Proprietário não encontrado")
    
    if usuario.id != propriedade.proprietario_id:
        usuario_antigo = Usuario.query.get(propriedade.proprietario_id)
        propriedade.proprietario_id = usuario.id
        if usuario not in propriedade.usuarios:
            propriedade.usuarios.append(usuario)
            propriedade.usuarios.remove(usuario_antigo)

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
    propriedade.usuarios.append(usuario)
    db.session.commit()
    return propriedade

  def remover_usuario(self, id: str, usuario_id: str):
    propriedade = self.__propriedade_existe(id)
    usuario = self.__usuario_existe(usuario_id)
    if usuario not in propriedade.usuarios:
      raise ConflictRequestError("Usuário não cadastrado na propriedade")

    propriedade.usuarios.remove(usuario)
    db.session.commit()
    return propriedade
  
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

  def __propriedade_existe(self, id):
    propriedade = Propriedade.query.get(id)
    if not propriedade:
      raise NotFoundRequestError("Propriedade nao encontrada")
    return propriedade

  def __get__perfil(self, id):
    perfil = Perfil.query.get(id)
    if not perfil:
      raise NotFoundRequestError("Perfil não encontrado")
    return perfil