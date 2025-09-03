from flask import request, jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required
from google.oauth2 import id_token
from google.auth.transport import requests
from app.exceptions.app_request_Exception import AppRequestError
from app.services.auth_service import AuthService


def register():
  # data = request.get_json()
  # try:
  #   nome = data.get('nome')
  #   email = data.get('email')
  #   senha = data.get('senha')
  #   return jsonify(
  #       AuthService().registrar_usuario(nome, email, senha)), 201
  # except AppRequestError as e:
  #   return jsonify(e.to_dict()), e.status_code
  return jsonify({
            "code": "BadRequestError",
            "message": "Registro de novos usuários está desabilitado.",
            "status": "301"
  }), 301


def login():
  data = request.get_json()
  email = data.get('email')
  senha = data.get('senha')
  try:
    return jsonify(AuthService().login(email, senha)), 200
  except AppRequestError as e:
    return jsonify(e.to_dict()), e.status_code


def authorize_google():
  # try:
  #   CLIENT_ID_GOOGLE = '18188128770-tpbogkb7i4f99c3o6701e2r25ap4jtes.apps.googleusercontent.com'
  #   dados = request.get_json()
  #   token_google = dados['token_google']
  #   idinfo = idinfo = id_token.verify_oauth2_token(token_google, requests.Request(), CLIENT_ID_GOOGLE)
  #   email = idinfo['email']
  #   nome = idinfo['name']
  #   return jsonify(AuthService().authorize_google(nome, email)), 200
  # except AppRequestError as e:
  #   return jsonify(e.to_dict()), e.status_code
  return jsonify({
            "code": "BadRequestError",
            "message": "Login social está desabilitado.",
            "status": "301"
  }), 301

def reset_password_request():
  dados = request.get_json()
  email = dados.get('email')

  try:
    return jsonify({"mensagem": AuthService().recuperar_senha(email)}), 200
  except AppRequestError as e:
    return jsonify(e.to_dict()), e.status_code


def reset_password():
  data = request.get_json()
  token = data.get('token')
  senha = data.get('senha')
  try:
    return jsonify({"mensagem": AuthService().resetar_senha(token, senha)}), 200
  except AppRequestError as e:
    return jsonify(e.to_dict()), e.status_code

 
@jwt_required(refresh=True)
def refresh_token():
  usuario_id = get_jwt_identity()
  try:
    return jsonify({'access_token': AuthService().refresh_token(usuario_id)}), 200
  except AppRequestError as e:
    return jsonify(e.to_dict()), e.status_code
