from flask import request, jsonify, url_for
from flask_jwt_extended import create_access_token
from app import db, google
from app.models.usuario_model import Usuario
from app.utils import default_perfil, reset_password

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
        description: Dados inválidos ou e-mail já cadastrado
        examples:
          application/json:
            erro: E-mail já cadastrado
    """
    
    data = request.get_json()

    if not all(k in data for k in ('nome', 'email', 'senha')):
        return jsonify({"erro": "Campos obrigatórios: nome, email, senha"}), 400

    if Usuario.query.filter_by(email=data['email']).first():
        return jsonify({"erro": "E-mail já cadastrado"}), 400

    data = request.get_json()
    nome = data.get('nome')
    email = data.get('email')
    senha = data.get('senha')

    perfil = default_perfil.default_perfil()
    usuario = Usuario(nome=nome, email=email, perfil_id=perfil.id)
    usuario.set_senha(senha)
    db.session.add(usuario)
    db.session.commit()
    
    return jsonify({"mensagem": "Usuário cadastrado com sucesso!"}), 201

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
        description: Falha na autenticação
        content:
          application/json:
            examples:
              usuario_nao_cadastrado:
                summary: Usuário não cadastrado
                value:
                  erro: Usuário não cadastrado
              usuario_desativado:
                summary: Usuário desativado
                value:
                  erro: Usuário desativado
              login_google:
                summary: Usuário cadastrado via Google
                value:
                  erro: Usuário cadastrado via Google, use o login com Google
              senha_invalida:
                summary: Email ou senha inválidos
                value:
                  erro: Email ou senha inválidos
    """
    data = request.get_json()
    email = data.get('email')
    senha = data.get('senha')

    usuario = Usuario.query.filter_by(email=email).first()
    
    if not usuario:
        return jsonify({'erro': 'Usuário não cadastrado'}), 401
    
    if usuario.is_active == False:
        return jsonify({'erro': 'Usuário desativado'}), 401
    
    if usuario.google_login == True:
        return jsonify({'erro': 'Usuário cadastrado via Google, use o login com Google'}), 401
    if usuario.is_active == False:
        return jsonify({'erro': 'Usuário desativado'}), 401
    
    if usuario and usuario.verificar_senha(senha):
        access_token = create_access_token(identity=str(usuario.id))
        return jsonify({'token': access_token}), 200

    return jsonify({'erro': 'Email ou senha inválidos'}), 401

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
    token = google.authorize_access_token()
    resp = google.get('userinfo')
    user_info = resp.json()
    
    email = user_info['email']
    nome = user_info.get('name', 'Usuário Google')

    usuario = Usuario.query.filter_by(email=email).first()
    
    if not usuario:
        perfil = default_perfil.default_perfil()
        usuario = Usuario(nome=nome, email=email, perfil_id=perfil.id, google_login=True) 
        db.session.add(usuario)
        db.session.commit()

    if usuario.is_active == False:
        return jsonify({'erro': 'Usuário desativado'}), 401
    if usuario.google_login == False:
        return jsonify({'erro': 'Usuário não cadastrado via Google'}), 401
    
    if usuario.is_active == False:
        return jsonify({'erro': 'Usuário desativado'}), 401
    
    access_token = create_access_token(identity=usuario.id)
    return jsonify({'token': access_token})
  
  
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
      401:
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

    usuario_existe = Usuario.query.filter_by(email=email).first()
    
    if not usuario_existe:
        return jsonify({'erro': 'E-mail não encontrado'}), 404
      
    if usuario_existe.is_active == False:
        return jsonify({'erro': 'Usuário desativado'}), 401
      
    if usuario_existe.google_login == True:
        return jsonify({'erro': 'Usuário cadastrado via Google'}), 401
        
    nova_senha = reset_password.gerar_nova_senha()
    usuario_existe.set_senha(nova_senha)
    nome = usuario_existe.nome
    db.session.commit()
    db.session.close()
    
    reset_password.enviar_senha(email, nova_senha, nome)
    return jsonify({'mensagem': 'Nova senha enviada para o e-mail.'})
  