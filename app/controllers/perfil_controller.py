from flask import request, jsonify
from app import db
from app.models.perfil_model import Perfil
from app.enum.PermissionEnum import PermissionEnum

def salvar_perfil():
    """
    Salva um novo perfil.
    ---
    tags:
      - Perfil
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
              example: "Administrador"
            permissoes:
              type: array
              example: ["USUARIO_LISTAR", "USUARIO_DETALHAR"]
    responses:
      201:
        description: Perfil criado com sucesso!
      400:
        description: O campo 'nome' é obrigatório
    """
    
    data = request.get_json()

    if 'nome' not in data:
        return jsonify({"erro": "O campo 'nome' é obrigatório"}), 400
    nome = data.get("nome")
    permissoes = [p.lower() for p in data.get("permissoes", [])]
    
    permissoes_validas = {perm.value for perm in PermissionEnum}
    permissoes_invalidas = [p for p in permissoes if p not in permissoes_validas]
    if permissoes_invalidas:
        return jsonify({"erro": f"Permissões inválidas: {permissoes_invalidas}"}), 400
      
    novo_perfil = Perfil(nome=nome, permissoes=permissoes)
    
    if db.session.query(Perfil).filter_by(nome=nome).first() is not None:
        return jsonify({"erro": "Ja existe um perfil com esse nome"}), 400
    
    db.session.add(novo_perfil)
    db.session.commit()

    return jsonify({"mensagem": "Perfil criado com sucesso!"}), 201

def listar_perfil():
    """
    Listar todos os perfis cadastrados.
    ---
    tags:
      - Perfil
    produces:
      - application/json
    responses:
      200:
        description: Lista de perfis retornada com sucesso.
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: integer
                example: 1
              nome:
                type: string
                example: "Administrador"
              permissoes:
                type: array
                items:
                  type: string
                example: ["USUARIO_LISTAR", "USUARIO_DETALHAR"]
    """
    
    perfis = Perfil.query.all()
    perfis_json = [
        {
            "id": perfil.id,
            "nome": perfil.nome,
            "permissoes": perfil.permissoes
        }
        for perfil in perfis
    ]
    return jsonify(perfis_json)
  

def atualizar_perfil(id):
    """
    Atualiza um perfil existente.
    ---
    tags:
      - Perfil
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
              example: "Novo Nome de Perfil"
            permissoes:
              type: array
              items:
                type: string
              example: ["USUARIO_LISTAR", "USUARIO_DETALHAR"]
    responses:
      200:
        description: Perfil atualizado com sucesso!
      400:
        description: Dados inválidos
      404:
        description: Perfil não encontrado
    """
    data = request.get_json()

    perfil = Perfil.query.get(id)
    if not perfil:
        return jsonify({"erro": "Perfil não encontrado"}), 404

    print(data.get("nome"))
    nome = data.get("nome")
    permissoes = [p.lower() for p in data.get("permissoes", [])]
    if not nome:
        return jsonify({"erro": "O campo 'nome' é obrigatório"}), 400

    permissoes_validas = {perm.value for perm in PermissionEnum}
    permissoes_invalidas = [p for p in permissoes if p not in permissoes_validas]
    if permissoes_invalidas:
        return jsonify({"erro": f"Permissões inválidas: {permissoes_invalidas}"}), 400

    perfil_existente = Perfil.query.filter_by(nome=nome).first()
    if perfil_existente and perfil_existente.id != perfil.id:
        return jsonify({"erro": "Já existe um perfil com esse nome"}), 400

    perfil.nome = nome
    perfil.permissoes = permissoes

    db.session.commit()

    return jsonify({"mensagem": "Perfil atualizado com sucesso!"}), 200