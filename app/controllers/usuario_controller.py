from flask import request, jsonify
from app import db
from app.exceptions import BadRequestError, ConflictRequestError, NotFoundRequestError
from app.models.usuario_model import Usuario
from app.models.perfil_model import Perfil
from app.utils.permissoes import permission_required, login_required
from app.enum.PermissionEnum import PermissionEnum
from app.services.usuario_service import UsuarioService


@login_required
@permission_required(PermissionEnum.USUARIO_CRIAR)
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
            id:
              type: string  # Mudado de integer para string (UUID)
              example: "51b03e1a-f849-438e-951a-f19a27b35902" 
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
              type: string 
              example: "1a7e8be3-b9b1-43a0-a04d-47dfb91372db" 
    responses:
      201:
        description: Usuário cadastrado com sucesso!
      400:
        description: Campos obrigatórios ausentes ou e-mail já cadastrado
"""
  data = request.get_json()

  try:
    nome = data.get('nome')
    email = data.get('email')
    senha = data.get('senha')
    perfil_id = data.get('perfil_id')
    return jsonify({
        'messagem':
        'Usuário cadastrado com sucesso',
        'data':
        UsuarioService.registrar_usuario(nome, email, senha, perfil_id).to_dict()
    }), 201
  except BadRequestError as e:
    return jsonify({"erro": e.message}), 400
  except ConflictRequestError as e:
    return jsonify({"erro": e.message}), 409
  except NotFoundRequestError as e:
    return jsonify({"erro": e.message}), 404


@login_required
@permission_required(PermissionEnum.USUARIO_LISTAR)
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
  return jsonify(UsuarioService.listar_usuarios()), 200


@login_required
@permission_required(PermissionEnum.USUARIO_EDITAR)
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
        type: string  # Mudado de integer para string (UUID)
        example: "51b03e1a-f849-438e-951a-f19a27b35902"  
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
              type: string  # Mudado de integer para string (UUID)
              example: "1a7e8be3-b9b1-43a0-a04d-47dfb91372db"  
    responses:
      200:
        description: Usuário atualizado com sucesso!
      404:
        description: Usuário não encontrado
"""

  data = request.get_json()

  try:
    return jsonify({
        "mensagem":
        "Usuário atualizado com sucesso!",
        "data":
        UsuarioService.atualizar_usuario(id, data['nome'], data['email'],
                                         data['perfil_id']).to_dict()
    }), 200
  except BadRequestError as e:
    return jsonify({"erro": e.message}), 400
  except ConflictRequestError as e:
    return jsonify({"erro": e.message}), 409
  except NotFoundRequestError as e:
    return jsonify({"erro": e.message}), 404

@login_required
@permission_required(PermissionEnum.USUARIO_EDITAR)
def status_usuario(id):
  """
    Ativar/Desativa um usuário existente.
    ---
    tags:
      - Usuários
    parameters:
      - in: path
        name: id
        required: true
        type: string  # Mudado de integer para string (UUID)
        example: "51b03e1a-f849-438e-951a-f19a27b35902"  
    responses:
      200:
        description: Usuário ativado/desativado com sucesso!
      404:
        description: Usuário nao encontrado
  """
  data = request.get_json()
  try:
    usuario = UsuarioService.status_usuario(id, data['status'])
    return jsonify({
        "mensagem":
        f"Usuário {'ativado' if usuario.is_active else 'desativado'} com sucesso!",
        "data":
        usuario.to_dict()
    }), 200
    
  except NotFoundRequestError as e:
    return jsonify({"erro": e.message}), 404
@login_required
@permission_required(PermissionEnum.USUARIO_DETALHAR)
def buscar_usuario(id):
  """
    Busca um usuário existente.
    ---
    tags:
      - Usuários
    parameters:
      - in: path
        name: id
        required: true
        type: string  # Mudado de integer para string (UUID)
        example: "51b03e1a-f849-438e-951a-f19a27b35902"  
    responses:
      200:
        description: Usuário encontrado com sucesso!
      404:
        description: Usuário nao encontrado
  """
  try:
    return jsonify(UsuarioService.buscar_usuario(id).to_dict()), 200
  except NotFoundRequestError as e:
    return jsonify({"erro": e.message}), 404
  
def relatorio_usuarios():
  return UsuarioService.relatorio_usuarios(), 200