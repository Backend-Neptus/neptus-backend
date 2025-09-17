from flask import request, jsonify
from app.enum.PermissionEnum import PermissionEnum
from app.exceptions.app_request_Exception import AppRequestError
from app.services.propriedade_service import PropriedadeService
from app.utils.permissoes import login_required, permission_required

@login_required
@permission_required(PermissionEnum.PROPRIEDADE_CRIAR)
def cadastrar_propriedade():
  data = request.get_json()
  try:
    nome = data.get('nome')
    proprietario_id = data.get('proprietario_id')
    return jsonify(
        PropriedadeService().cadastrar_propriedade(nome,
                                                   proprietario_id).to_dict()
    ), 201
  except AppRequestError as e:
    return jsonify(e.to_dict()), e.status_code


@login_required
@permission_required(PermissionEnum.PROPRIEDADE_LISTAR)
def listar_propriedades():
  page = request.args.get('page', 1, type=int)
  per_page = request.args.get('per_page', 10, type=int)
  return jsonify(PropriedadeService().listar_propriedades(page, per_page)), 200

@login_required
@permission_required(PermissionEnum.PROPRIEDADE_EDITAR)
def atualizar_propriedade(id):
  data = request.get_json()
  nome = data.get('nome')
  proprietario_id = data.get('proprietario_id')
  print(id)
  try:
    return jsonify(
        PropriedadeService().atualizar_propriedade(
            id, nome, proprietario_id).to_dict()
    ), 200
  except AppRequestError as e:
    return jsonify(e.to_dict()), e.status_code


@login_required
@permission_required(PermissionEnum.PROPRIEDADE_LISTAR)
def detalhar_propriedade(id):
  try:
    return jsonify(
        PropriedadeService().detalhar_propriedade(id).to_dict()), 200
  except AppRequestError as e:
    return jsonify(e.to_dict()), e.status_code



@login_required
def adicionar_usuario():
  """
  Adiciona um usuario a uma propriedade.
  ---
  tags:
    - Propriedade
  responses:
    200:
      description: Usuario adicionado a propriedade
      examples:
        application/json:
          mensagem: Usuario adicionado a propriedade
  """
  data = request.get_json()
  id_propriedade = data.get('propriedade_id')
  id_usuario = data.get('usuario_id')
  try:
    return jsonify(
        PropriedadeService().adicionar_usuario(id_propriedade,
                                               id_usuario).to_dict()
    ), 200
  except AppRequestError as e:
    return jsonify(e.to_dict()), e.status_code


@login_required
def remover_usuario():
  """
  Remove um usuario de uma propriedade.
  ---
  tags:
    - Propriedade
  responses:
    200:
      description: Usuario removido da propriedade
      examples:
        application/json:
          mensagem: Usuario removido da propriedade
  """
  data = request.get_json()
  id_propriedade = data.get('propriedade_id')
  id_usuario = data.get('usuario_id')
  try:
    return jsonify(
        PropriedadeService().remover_usuario(id_propriedade,
                                             id_usuario).to_dict()
    ), 200
  except AppRequestError as e:
    return jsonify(e.to_dict()), e.status_code



