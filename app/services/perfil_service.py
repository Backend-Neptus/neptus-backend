from app import db
from app.exceptions import BadRequestError, ConflictRequestError, NotFoundRequestError
from app.models.perfil_model import Perfil
from app.enum.PermissionEnum import PermissionEnum
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

    if db.session.query(Perfil).filter_by(nome=nome).first() is not None:
      raise ConflictRequestError("Perfil com esse nome ja cadastrado")

    perfil = Perfil(nome=nome, permissoes=permissoes)
    db.session.add(perfil)
    db.session.commit()

    return perfil

  def listar_perfis():
    return [{
        "id": perfil.id,
        "nome": perfil.nome,
        "permissoes": perfil.permissoes,
        "usuarios": len(perfil.usuarios)
    } for perfil in Perfil.query.all()]

  def atualizar_perfil(id, nome, permissoes):
    perfil = Perfil.query.filter_by(id=id).first()

    perfil_default = get_default_perfil()
    if perfil.id == perfil_default.id:
      if nome != perfil_default.nome:
        raise BadRequestError("O campo 'nome' nao pode ser alterado para o perfil default")
    
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

    perfil_existente = Perfil.query.filter_by(nome=nome).first()
    if perfil_existente and perfil_existente.id != perfil.id:
      raise ConflictRequestError("Perfil com esse nome ja cadastrado")

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