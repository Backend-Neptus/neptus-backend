from flask import request, jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required
from app.exceptions.app_request_Exception import AppRequestError
from app.services.auth_service import AuthService


def register():
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
