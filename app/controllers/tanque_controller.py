from flask import request, jsonify
from app.services.tanque_service import TanqueService
from app.exceptions import BadRequestError, NotFoundRequestError, ConflictRequestError
from app.utils.permissoes import permission_required, login_required
from app.enum.PermissionEnum import PermissionEnum

@login_required
@permission_required(PermissionEnum.TANQUE_CRIAR)
def cadastrar_tanque():
    """
    Cadastra um novo tanque.
    ---
    tags:
      - Tanque
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
              example: "Tanque 1"
            propriedade_id:
              type: string
              example: "a1b2c3d4-e5f6-7890-1234-567890abcdef"
            status:
              type: string
              example: "Ativo"
    responses:
      201:
        description: Tanque cadastrado com sucesso!
      400:
        description: Dados inválidos
      404:
        description: Propriedade não encontrada
      409:
        description: Tanque com o mesmo nome já cadastrado
    """
    data = request.get_json()
    try:
        nome = data.get('nome')
        propriedade_id = data.get('propriedade_id')
        return jsonify({'mensagem': 'Tanque cadastrado com sucesso!', 'tanque': TanqueService().cadastrar_tanque(nome, propriedade_id).to_dict()}), 201

    except BadRequestError as e:
        return jsonify({'erro': e.message}), 400
    except NotFoundRequestError as e:
        return jsonify({'erro': e.message}), 404
    except ConflictRequestError as e:
        return jsonify({'erro': e.message}), 409

@login_required
@permission_required(PermissionEnum.TANQUE_LISTAR)
def listar_tanques():
    """
    Lista todos os tanques.
    ---
    tags:
      - Tanque
    responses:
      200:
        description: Lista de tanques
    """
    tanques = TanqueService().listar_tanques()
    return jsonify([tanque.to_dict() for tanque in tanques]), 200

@login_required
@permission_required(PermissionEnum.TANQUE_DETALHAR)
def detalhar_tanque(id):
    """
    Detalha um tanque específico.
    ---
    tags:
      - Tanque
    parameters:
      - in: path
        name: id
        required: true
        type: string
        description: ID do tanque a ser detalhado
    responses:
      200:
        description: Detalhes do tanque
      404:
        description: Tanque não encontrado
    """
    try:
        tanque = TanqueService().detalhar_tanque(id)
        return jsonify(tanque.to_dict()), 200
    except NotFoundRequestError as e:
        return jsonify({'erro': e.message}), 404

@login_required
@permission_required(PermissionEnum.TANQUE_EDITAR)
def atualizar_tanque(id):
    """
    Atualiza um tanque existente.
    ---
    tags:
      - Tanque
    parameters:
      - in: path
        name: id
        required: true
        type: string
        description: ID do tanque a ser atualizado
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            nome:
              type: string
              example: "Novo Nome do Tanque"
            propriedade_id:
              type: string
              example: "a1b2c3d4-e5f6-7890-1234-567890abcdef"
            status:
              type: string
              example: "Inativo"
    responses:
      200:
        description: Tanque atualizado com sucesso
      400:
        description: Dados inválidos
      404:
        description: Tanque ou propriedade não encontrada
      409:
        description: Tanque com o mesmo nome já cadastrado
    """
    data = request.get_json()
    try:
        nome = data.get('nome')
        propriedade_id = data.get('propriedade_id')
        status = data.get('status')

        tanque = TanqueService().atualizar_tanque(id, nome, propriedade_id, status)
        return jsonify({'mensagem': 'Tanque atualizado com sucesso!', 'tanque': tanque.to_dict()}), 200

    except BadRequestError as e:
        return jsonify({'erro': e.message}), 400
    except NotFoundRequestError as e:
        return jsonify({'erro': e.message}), 404
    except ConflictRequestError as e:
        return jsonify({'erro': e.message}), 409

@login_required
@permission_required(PermissionEnum.TANQUE_EXCLUIR)
def deletar_tanque(id):
    """
    Deleta um tanque existente.
    ---
    tags:
      - Tanque
    parameters:
      - in: path
        name: id
        required: true
        type: string
        description: ID do tanque a ser deletado
    responses:
      200:
        description: Tanque deletado com sucesso
      404:
        description: Tanque não encontrado
    """
    try:
        TanqueService().deletar_tanque(id)
        return jsonify({'mensagem': 'Tanque deletado com sucesso!'}), 200

    except NotFoundRequestError as e:
        return jsonify({'erro': e.message}), 404