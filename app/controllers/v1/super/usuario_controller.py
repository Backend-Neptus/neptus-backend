from flask import request, jsonify
from app import db
from app.exceptions import BadRequestError, ConflictRequestError, NotFoundRequestError
from app.exceptions.app_request_Exception import AppRequestError
from app.models.usuario_model import Usuario
from app.models.perfil_model import Perfil
from app.utils.permissoes import permission_required, login_required
from app.enum.PermissionEnum import PermissionEnum
from app.services.usuario_service import UsuarioService


def salvar_usuario():
  data = request.get_json()
  try:
    nome = data.get('nome')
    email = data.get('email')
    senha = data.get('senha')
    perfil_id = data.get('perfil_id')
    return jsonify(
        UsuarioService.registrar_usuario(nome, email, senha, perfil_id).to_dict()
    ), 201
  except AppRequestError as e:
    return jsonify(e.to_dict()), e.status_code

@login_required
@permission_required(PermissionEnum.USUARIO_LISTAR)
def listar_usuarios():
  page = request.args.get('pagina_atual', 1, type=int)
  per_page = request.args.get('itens_por_pagina', 10, type=int)
  return jsonify(UsuarioService.listar_usuarios(page, per_page)), 200

@login_required
@permission_required(PermissionEnum.USUARIO_EDITAR)
def atualizar_usuario(id):
  data = request.get_json()
  try:
    nome = data.get('nome')
    email = data.get('email')
    perfil_id = data.get('perfil_id')
    return jsonify(
        UsuarioService.atualizar_usuario(id, nome, email,
                                         perfil_id).to_dict()
    ), 200
  except AppRequestError as e:
    return jsonify(e.to_dict()), e.status_code


@login_required
@permission_required(PermissionEnum.USUARIO_EDITAR)
def status_usuario(id):
  data = request.get_json()
  status = data.get('status')
  try:
    return jsonify(UsuarioService.status_usuario(id, status)), 200
  except AppRequestError as e:
    return jsonify(e.to_dict()), e.status_code

@login_required
@permission_required(PermissionEnum.USUARIO_DETALHAR)
def buscar_usuario(id):
  try:
    return jsonify(UsuarioService.buscar_usuario(id).to_dict()), 200
  except AppRequestError as e:
    return jsonify(e.to_dict()), e.status_code

def relatorio_usuarios():
  return jsonify(UsuarioService.relatorio_usuarios()), 200