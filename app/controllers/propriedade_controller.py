from flask import request, jsonify, url_for
from flask_jwt_extended import get_jwt_identity, jwt_required
from app import google
from app.exceptions import (BadRequestError, ConflictRequestError,
                            UserDisabledError, GoogleLoginRequestError,
                            NotFoundRequestError, InvalidCredentialsError)
from app.services.propriedade_service import PropriedadeService
from app.utils.permissoes import login_required


def cadastrar_propriedade():
  """
Cadastra uma nova propriedade.
---
tags:
  - Propriedade
parameters:
  - in: body
    name: corpo
    required: true
    schema:
      type: object
      required:
        - nome
        - proprietario_id
      properties:
        nome:
          type: string
          example: Fazenda Boa Vista
        proprietario_id:
          type: string
          format: uuid
          example: "0d8fbbb3-77dc-42a4-bb88-1de12fb7395f"
responses:
  200:
    description: Propriedade cadastrada com sucesso
    examples:
      application/json:
        mensagem: Propriedade cadastrada com sucesso
        data:
          id: "b0ec1d2e-9b0f-4d42-bf89-8db3c32c48e9"
          nome: Fazenda Boa Vista
          total_usuarios: 1
          usuarios:
            - id: "0d8fbbb3-77dc-42a4-bb88-1de12fb7395f"
              nome: João da Silva
              email: joao@email.com
          proprietario_id: "0d8fbbb3-77dc-42a4-bb88-1de12fb7395f"
          proprietario_nome: João da Silva
          created_at: "14/04/2025 12:00:00"
          updated_at: "14/04/2025 12:00:00"
  404:
    description: Proprietário não encontrado ou campos inválidos
    examples:
      application/json:
        erro: Proprietário não encontrado
  409:
    description: Propriedade com mesmo nome já cadastrada
    examples:
      application/json:
        erro: Propriedade com mesmo nome já cadastrada
"""
  data = request.get_json()
  try:
    nome = data.get('nome')
    proprietario_id = data.get('proprietario_id')
    return jsonify({
        'messagem':
        'Propriedade cadastrada com sucesso',
        'data':
        PropriedadeService().cadastrar_propriedade(nome,
                                                   proprietario_id).to_dict()
    }), 200
  except ConflictRequestError as e:
    return jsonify({'erro': e.message}), 409
  except NotFoundRequestError as e:
    return jsonify({'erro': e.message}), 404
  except BadRequestError as e:
    return jsonify({'erro': e.message}), 404


def listar_propriedades():
  """
Lista todas as propriedades cadastradas.
---
tags:
  - Propriedade
responses:
  200:
    description: Lista de propriedades
    examples:
      application/json:
        - id: "b0ec1d2e-9b0f-4d42-bf89-8db3c32c48e9"
          nome: Fazenda Boa Vista
          total_usuarios: 2
          usuarios:
            - id: "0d8fbbb3-77dc-42a4-bb88-1de12fb7395f"
              nome: João da Silva
              email: joao@email.com
          proprietario_id: "0d8fbbb3-77dc-42a4-bb88-1de12fb7395f"
          proprietario_nome: João da Silva
          created_at: "14/04/2025 12:00:00"
          updated_at: "14/04/2025 12:00:00"
"""
  return jsonify(PropriedadeService().listar_propriedades()), 200


def atualizar_propriedade(id):
  """
Atualiza uma propriedade existente.
---
tags:
  - Propriedade
parameters:
  - in: path
    name: id
    required: true
    type: string
    format: uuid
    description: ID da propriedade a ser atualizada
    example: "b0ec1d2e-9b0f-4d42-bf89-8db3c32c48e9"
  - in: body
    name: corpo
    required: true
    schema:
      type: object
      required:
        - nome
        - proprietario_id
      properties:
        nome:
          type: string
          example: Fazenda Atualizada
        proprietario_id:
          type: string
          format: uuid
          example: "0d8fbbb3-77dc-42a4-bb88-1de12fb7395f"
responses:
  200:
    description: Propriedade atualizada com sucesso
    examples:
      application/json:
        mensagem: Propriedade atualizada com sucesso
        data:
          id: "b0ec1d2e-9b0f-4d42-bf89-8db3c32c48e9"
          nome: Fazenda Atualizada
          total_usuarios: 2
          usuarios:
            - id: "0d8fbbb3-77dc-42a4-bb88-1de12fb7395f"
              nome: João da Silva
              email: joao@email.com
          proprietario_id: "0d8fbbb3-77dc-42a4-bb88-1de12fb7395f"
          proprietario_nome: João da Silva
          created_at: "14/04/2025 12:00:00"
          updated_at: "14/04/2025 12:10:00"
  404:
    description: Propriedade ou proprietário não encontrado
    examples:
      application/json:
        erro: Propriedade nao encontrada
  409:
    description: Propriedade com mesmo nome já cadastrada
    examples:
      application/json:
        erro: Propriedade com mesmo nome já cadastrada
"""
  data = request.get_json()
  try:
    return jsonify({
        'messagem':
        'Propriedade atualizada com sucesso',
        'data':
        PropriedadeService().atualizar_propriedade(
            id, data.get('nome'), data.get('proprietario_id')).to_dict()
    }), 200
  except ConflictRequestError as e:
    return jsonify({'erro': e.message}), 409
  except NotFoundRequestError as e:
    return jsonify({'erro': e.message}), 404
  except BadRequestError as e:
    return jsonify({'erro': e.message}), 404


def detalhar_propriedade(id):
  """
  Detalha uma propriedade.
  ---
  tags:
    - Propriedade
  responses:
    200:
      description: Lista de propriedades
      examples:
        application/json:
          - id: "b0ec1d2e-9b0f-4d42-bf89-8db3c32c48e9"
            nome: Fazenda Boa Vista
            total_usuarios: 2
            usuarios:
              - id: "0d8fbbb3-77dc-42a4-bb88-1de12fb7395f"
                nome: João da Silva
                email: joao@email.com
            proprietario_id: "0d8fbbb3-77dc-42a4-bb88-1de12fb7395f"
            proprietario_nome: João da Silva
            created_at: "14/04/2025 12:00:00"
            updated_at: "14/04/2025 12:00:00"
  """
  try:
    return jsonify(
        {'data': PropriedadeService().detalhar_propriedade(id).to_dict()}), 200
  except NotFoundRequestError as e:
    return jsonify({'erro': e.message}), 404


@login_required
def adicionar_usuario():
  """
  Adiciona um usuario a uma propriedade.
  ---
  tags:
    - Propriedade
  responses:
    200:
      description: Usuario adicionado a propriedade
      examples:
        application/json:
          mensagem: Usuario adicionado a propriedade
  """
  data = request.get_json()
  id_propriedade = data.get('propriedade_id')
  id_usuario = data.get('usuario_id')
  try:
    return jsonify({
        'mensagem':
        "Usuario adicionado a propriedade",
        'data':
        PropriedadeService().adicionar_usuario(id_propriedade,
                                               id_usuario).to_dict()
    }), 200
  except NotFoundRequestError as e:
    return jsonify({'erro': e.message}), 404
  except BadRequestError as e:
    return jsonify({
        'erro': "Erro inesperado no servidor",
        'detalhes': str(e)
    }), 403
  except ConflictRequestError as e:
    return jsonify({'erro': e.message}), 409
  except Exception as e:
    return jsonify({
        'erro': "Erro inesperado no servidor",
        'detalhes': str(e)
    }), 500

@login_required
def remover_usuario():
  """
  Remove um usuario de uma propriedade.
  ---
  tags:
    - Propriedade
  responses:
    200:
      description: Usuario removido da propriedade
      examples:
        application/json:
          mensagem: Usuario removido da propriedade
  """
  data = request.get_json()
  id_propriedade = data.get('propriedade_id')
  id_usuario = data.get('usuario_id')
  try:
    return jsonify({
        'mensagem':
        "Usuario removido da propriedade",
        'data':
        PropriedadeService().remover_usuario(id_propriedade,
                                               id_usuario).to_dict()
    }), 200
  except NotFoundRequestError as e:
    return jsonify({'erro': e.message}), 404
  except BadRequestError as e:
    return jsonify({
        'erro': "Erro inesperado no servidor",
        'detalhes': str(e)
    }), 403
  except ConflictRequestError as e:
    return jsonify({'erro': e.message}), 409
  except Exception as e:
    return jsonify({
        'erro': "Erro inesperado no servidor",
        'detalhes': str(e)
    }), 500