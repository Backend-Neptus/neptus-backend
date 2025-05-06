from flask import request, jsonify
from app.enum.PermissionEnum import PermissionEnum
from app.exceptions import (BadRequestError, ConflictRequestError,
                            NotFoundRequestError)
from app.exceptions.app_request_Exception import AppRequestError
from app.services.perfil_service import PerfilService
from app.services.propriedade_service import PropriedadeService
from app.utils.permissoes import login_required, permission_required


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
  except AppRequestError as e:
    return jsonify(e.to_dict()), e.status_code



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
  except AppRequestError as e:
    return jsonify(e.to_dict()), e.status_code



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
  except AppRequestError as e:
    return jsonify(e.to_dict()), e.status_code



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
  except AppRequestError as e:
    return jsonify(e.to_dict()), e.status_code


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
  except AppRequestError as e:
    return jsonify(e.to_dict()), e.status_code



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
        PropriedadeService().convite_aceito(token_convite).to_dict()
    }), 200
  except AppRequestError as e:
    return jsonify(e.to_dict()), e.status_code

# TESTE DE PERFIL LOCAIS 
# IMPLEMENTANDO SISTEMA DE LOGIN PARA PROPRIEDADE (PERFIL LOCAL)
@login_required
def salvar_perfil_local():
  data = request.get_json()
  try:
    nome = data.get("nome")
    propriedade_id = data.get("propriedade_id")
    permissoes = data.get("permissoes", [])
    return jsonify(PropriedadeService.salvar_perfil_local(nome, permissoes, propriedade_id).to_dict()), 201
  except AppRequestError as e:
    return jsonify(e.to_dict()), e.status_code


@login_required
def atualizar_perfil_local():
  data = request.get_json()
  try:
    usuario_id = data.get("usuario_id")
    propriedade_id = data.get("propriedade_id")
    perfil_id = data.get("perfil_id")
    return jsonify({"mensagem":PropriedadeService().autalizar_perfil_local_usuario(propriedade_id, perfil_id, usuario_id)}), 201
  except AppRequestError as e:
    return jsonify(e.to_dict()), e.status_code

