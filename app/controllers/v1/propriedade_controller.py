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
