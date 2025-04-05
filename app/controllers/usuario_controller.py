from flask import request, jsonify
from app import db
from app.models.usuario_model import Usuario
from app.models.perfil_model import Perfil  # Não esquecer de importar!


def salvar_usuario():
    """
    Cadastra um novo usuário.
    ---
    tags:
      - Usuários
    consumes:
      - application/json
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            nome:
              type: string
              example: "Guido van Rossum"
            email:
              type: string
              example: "email@example.com"
            senha:
              type: string
              example: "123456"
            perfil_id:
              type: integer
              example: 1
    responses:
      201:
        description: Usuário cadastrado com sucesso!
      400:
        description: Campos obrigatórios ausentes ou e-mail já cadastrado
    """
    data = request.get_json()

    if not all(k in data for k in ('nome', 'email', 'senha', 'perfil_id')):
        return jsonify({"erro": "Campos obrigatórios: nome, email, senha, perfil_id"}), 400

    if Usuario.query.filter_by(email=data['email']).first():
        return jsonify({"erro": "E-mail já cadastrado"}), 400

    # Verifica se o perfil existe
    perfil = Perfil.query.get(data['perfil_id'])
    if not perfil:
        return jsonify({'erro': 'Perfil não encontrado'}), 404

    novo_usuario = Usuario(
        nome=data['nome'],
        email=data['email'],
        perfil_id=data['perfil_id']
    )
    novo_usuario.set_senha(data['senha'])

    db.session.add(novo_usuario)
    db.session.commit()

    return jsonify({"mensagem": "Usuário cadastrado com sucesso!"}), 201


def listar_usuarios():
    """
    Lista todos os usuários cadastrados.
    ---
    tags:
      - Usuários
    responses:
      200:
        description: Lista de usuários
    """
    usuarios = Usuario.query.all()
    resultado = []

    for usuario in usuarios:
        resultado.append({
            'id': usuario.id,
            'nome': usuario.nome,
            'email': usuario.email,
            'perfil_id': usuario.perfil_id
        })

    return jsonify(resultado), 200


def atualizar_usuario(id):
    """
    Atualiza os dados de um usuário existente.
    ---
    tags:
      - Usuários
    parameters:
      - in: path
        name: id
        required: true
        type: integer
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            nome:
              type: string
              example: "Novo Nome"
            email:
              type: string
              example: "novo@email.com"
            senha:
              type: string
              example: "nova_senha"
            perfil_id:
              type: integer
              example: 2
    responses:
      200:
        description: Usuário atualizado com sucesso!
      404:
        description: Usuário não encontrado
    """
    usuario = Usuario.query.get(id)

    if not usuario:
        return jsonify({"erro": "Usuário não encontrado"}), 404

    data = request.get_json()

    if 'nome' in data:
        usuario.nome = data['nome']
    if 'email' in data:
        usuario.email = data['email']
    if 'senha' in data:
        usuario.set_senha(data['senha'])
    if 'perfil_id' in data:
        # Verifica se o perfil existe antes de atualizar
        perfil = Perfil.query.get(data['perfil_id'])
        if not perfil:
            return jsonify({'erro': 'Perfil não encontrado'}), 404
        usuario.perfil_id = data['perfil_id']

    db.session.commit()

    return jsonify({"mensagem": "Usuário atualizado com sucesso!"}), 200
