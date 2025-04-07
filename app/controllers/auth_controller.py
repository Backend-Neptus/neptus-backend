from flask import request, jsonify, url_for
from app import google
from app.exceptions import (BadRequestError, ConflictRequestError,
                            UserDisabledError, GoogleLoginRequestError,
                            NotFoundRequestError, InvalidCredentialsError)
from app.services.auth_service import AuthService


def register():
  """
    Cadastra um novo usuário.
    ---
    tags:
      - Autenticação
    parameters:
      - in: body
        name: corpo
        required: true
        schema:
          type: object
          required:
            - nome
            - email
            - senha
          properties:
            nome:
              type: string
              example: João da Silva
            email:
              type: string
              example: joao@email.com
            senha:
              type: string
              example: 123456
    responses:
      201:
        description: Usuário cadastrado com sucesso
        examples:
          application/json:
            mensagem: Usuário cadastrado com sucesso!
      400:
        description: Os campos 'nome', 'email' e 'senha' devem ser preenchidos
        examples:
          application/json:
            erro: Os campos 'nome', 'email' e 'senha' devem ser preenchidos
      409:
        description: E-mail ja cadastrado
        examples:
          application/json:
            erro: E-mail ja cadastrado
    """
  data = request.get_json()
  try:
    nome = data.get('nome')
    email = data.get('email')
    senha = data.get('senha')
    return jsonify({'token': AuthService().registrar_usuario(nome, email, senha)}), 201
  except BadRequestError as e:
    return jsonify({"erro": e.message}), 400
  except ConflictRequestError as e:
    return jsonify({"erro": e.message}), 409


def login():
  """
    Realiza o login com e-mail e senha.
    ---
    tags:
      - Autenticação
    parameters:
      - in: body
        name: corpo
        required: true
        schema:
          type: object
          required:
            - email
            - senha
          properties:
            email:
              type: string
              example: joao@email.com
            senha:
              type: string
              example: 123456
    responses:
      200:
        description: Login realizado com sucesso
        examples:
          application/json:
            token: eyJ0eXAiOiJKV1QiLCJhbGciOi...
      401:
        description: Usuário não cadastrado ou Email ou senha inválidos
        examples:
          application/json:
            erro: Usuário não cadastrado ou Email ou senha inválidos
      403:
        description: Usuário desativado ou cadastrado via Google
        examples:
          application/json:
            erro: Usuário desativado ou cadastrado via Google
    """
  data = request.get_json()
  email = data.get('email')
  senha = data.get('senha')
  try:
    return jsonify({'token': AuthService().login(email, senha)}), 200
  except NotFoundRequestError as e:
    return jsonify({"erro": e.message}), 401
  except UserDisabledError as e:
    return jsonify({"erro": e.message}), 403
  except GoogleLoginRequestError as e:
    return jsonify({"erro": e.message}), 403
  except InvalidCredentialsError as e:
    return jsonify({"erro": e.message}), 401


def login_google():
  """
    Inicia o processo de login com o Google.
    ---
    tags:
      - Autenticação
    responses:
      302:
        description: Redireciona para o login do Google
    """
  redirect_uri = url_for('authorize_google', _external=True)
  return google.authorize_redirect(redirect_uri)


def authorize_google():
  """
    login com o Google.
    ---
    tags:
      - Autenticação
    responses:
      200:
        description: Login realizado com sucesso
        examples:
          application/json:
            token: eyJ0eXAiOiJKV1QiLCJhbGciOi...
      403:
        description: Usuário desativado ou não cadastrado via Google
        examples:
          application/json:
            erro: Usuário desativado ou não cadastrado via Google
  """
  google.authorize_access_token()
  resp = google.get('userinfo')
  user_info = resp.json()

  email = user_info['email']
  nome = user_info.get('name', 'Usuário Google')
  try:
    return jsonify({'token': AuthService().authorize_google(nome, email)}), 200
  except UserDisabledError as e:
    return jsonify({'erro': e.message}), 403
  except GoogleLoginRequestError as e:
    return jsonify({'erro': e.message}), 403


def reset_password_request():
  """
    Gera uma nova senha e envia para o e-mail informado.
    ---
    tags:
      - Autenticação
    parameters:
      - in: body
        name: corpo
        required: true
        schema:
          type: object
          properties:
            email:
              type: string
              example: usuario@exemplo.com
    responses:
      200:
        description: Nova senha enviada com sucesso.
        examples:
          application/json:
            mensagem: Nova senha enviada para o e-mail.
      403:
        description: Usuário desativado ou cadastrado via Google.
        examples:
          application/json:
            erro: Usuário desativado
      404:
        description: E-mail não encontrado.
        examples:
          application/json:
            erro: E-mail não encontrado
    """
  dados = request.get_json()
  email = dados.get('email')

  try:
    return jsonify({"mensagem": AuthService().recuperar_senha(email)}), 200
  except NotFoundRequestError as e:
    return jsonify({"erro": str(e)}), 404
  except UserDisabledError as e:
    return jsonify({"erro": str(e)}), 403
  except GoogleLoginRequestError as e:
    return jsonify({"erro": str(e)}), 403
