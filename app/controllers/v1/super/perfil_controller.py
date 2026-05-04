from flask import request, jsonify
from app import db
from app.exceptions import BadRequestError, ConflictRequestError, NotFoundRequestError
from app.exceptions.app_request_Exception import AppRequestError
from app.models.perfil_model import Perfil
from app.enum.PermissionEnum import PermissionEnum
from app.models.usuario_model import Usuario
from app.services.perfil_service import PerfilService
from app.utils.permissoes import permission_required, login_required


@login_required
@permission_required(PermissionEnum.PERFIL_CRIAR)
def salvar_perfil():
  data = request.get_json()
  try:
    nome = data.get("nome")
    permissoes = data.get("permissoes", [])
    return jsonify(PerfilService.criar_perfil(nome, permissoes).to_dict()), 201
  except AppRequestError as e:
    return jsonify(e.to_dict()), e.status_code

@login_required
@permission_required(PermissionEnum.PERFIL_LISTAR)
def listar_perfil():
  page = request.args.get('page', 1, type=int)
  per_page = request.args.get('per_page', 10, type=int)
  return jsonify(PerfilService.listar_perfis(page, per_page)), 200

@login_required
@permission_required(PermissionEnum.PERFIL_EDITAR)
def atualizar_perfil(id):
  data = request.get_json()
  try:
    nome = data.get("nome")
    permissoes = data.get("permissoes", [])
    return jsonify(
        PerfilService.atualizar_perfil(id, nome, permissoes).to_dict()
    ), 200
  except AppRequestError as e:
    return jsonify(e.to_dict()), e.status_code


@login_required
@permission_required(PermissionEnum.PERFIL_EXCLUIR)
def deletar_perfil(id):
  try:
    return jsonify({'messagem': PerfilService.deletar_perfil(id)}), 200
  except AppRequestError as e:
    return jsonify(e.to_dict()), e.status_code


@login_required
@permission_required(PermissionEnum.PERFIL_DETALHAR)
def buscar_perfil(id):
  try:
    return jsonify(PerfilService.buscar_perfil(id).to_dict()), 200
  except AppRequestError as e:
    return jsonify(e.to_dict()), e.status_code



