from app import db
from app.exceptions import BadRequestError, ConflictRequestError, NotFoundRequestError
from app.models.perfil_model import Perfil
from app.enum.PermissionEnum import PermissionEnum
from app.models.propriedade_model import Propriedade
from app.utils.default_perfil import get_default_perfil


class PerfilService:

  def criar_perfil(nome, permissoes):

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

    perfil = Perfil(nome=nome, permissoes=permissoes)
    db.session.add(perfil)
    db.session.commit()

    return perfil

  def listar_perfis(page, per_page):
    if per_page > 50:
      per_page = 50
    perfis = Perfil.query.order_by(Perfil.criado_em).paginate(
        page=page, per_page=per_page, error_out=False)
    return {
        'total': perfis.total,
        'pagina_atual': perfis.page,
        'itens_por_pagina': perfis.per_page,
        'total_paginas': perfis.pages,
        'perfis': [perfil.to_dict() for perfil in perfis]
    }
  
  def atualizar_perfil(id, nome, permissoes):
    perfil = Perfil.query.filter_by(id=id).first()

    perfil_default = get_default_perfil()
    if perfil.id == perfil_default.id:
      if nome != perfil_default.nome:
        raise BadRequestError("O campo 'nome' não pode ser alterado para o perfil default")
    
    if not perfil:
      raise NotFoundRequestError("Perfil nao encontrado")

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

    perfil.nome = nome
    perfil.permissoes = permissoes

    db.session.commit()

    return perfil

  def deletar_perfil(id):
    perfil = Perfil.query.filter_by(id=id).first()

    if not perfil:
      raise NotFoundRequestError("Perfil nao encontrado")

    perfil_default = get_default_perfil()
    if perfil.id == perfil_default.id:
      raise BadRequestError("Perfil default nao pode ser deletado")

    for usuario in perfil.usuarios:
      usuario.perfil_id = perfil_default.id
      
    db.session.commit()
    db.session.delete(perfil)
    db.session.commit()

    return "perfil deletado com sucesso! todos os usuarios foram transferidos para o perfil default"
  
  def buscar_perfil(id):
    perfil = Perfil.query.filter_by(id=id).first()
    if not perfil:
      raise NotFoundRequestError("Perfil nao encontrado")
    return perfil
  
