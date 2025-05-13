from flask import request, jsonify
from app.exceptions.app_request_Exception import AppRequestError
from app.services.propriedade_service import PropriedadeService
from app.utils.permissoes import login_required


##########################################################
###                                                    ###
###Esta é uma rota de acesso vinculada ao perfil local.###
###                                                    ###
##########################################################


@login_required
def convidar_usuario():
  data = request.get_json()
  id_propriedade = data.get('propriedade_id')
  email = data.get('email')
  try:
    return jsonify({
        'mensagem':
        PropriedadeService().convidar_usuario(id_propriedade, email)
    }), 200
  except AppRequestError as e:
    return jsonify(e.to_dict()), e.status_code



def convite_aceito():
  data = request.get_json()
  token_convite = data.get('token_convite')
  try:
    return jsonify({
        'mensagem':
        PropriedadeService().convite_aceito(token_convite)
    }), 200
  except AppRequestError as e:
    return jsonify(e.to_dict()), e.status_code

@login_required
def criar_perfil_local():
  data = request.get_json()
  try:
    nome = data.get("nome")
    propriedade_id = data.get("propriedade_id")
    permissoes = data.get("permissoes", [])
    return jsonify(PropriedadeService().salvar_perfil_local(nome, permissoes, propriedade_id).to_dict()), 201
  except AppRequestError as e:
    return jsonify(e.to_dict()), e.status_code

@login_required
def atualizar_perfil_local(id):
  data = request.get_json()
  try:
    propriedade_id = data.get("propriedade_id")
    nome = data.get("nome")
    permissoes = data.get("permissoes", [])
    return jsonify({"mensagem": PropriedadeService().atualizar_perfil_local(id, nome, permissoes, propriedade_id)}), 201
  except AppRequestError as e:
    return jsonify(e.to_dict()), e.status_code


@login_required
def atualizar_perfil_usuario():
  data = request.get_json()
  try:
    usuario_id = data.get("usuario_id")
    propriedade_id = data.get("propriedade_id")
    perfil_id = data.get("perfil_id")
    return jsonify({"mensagem":PropriedadeService().autalizar_perfil_local_usuario(propriedade_id, perfil_id, usuario_id)}), 201
  except AppRequestError as e:
    return jsonify(e.to_dict()), e.status_code
