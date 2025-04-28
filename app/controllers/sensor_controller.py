from flask import request, jsonify
from app.services.sensor_service import SensorService
from app.exceptions import BadRequestError, NotFoundRequestError, ConflictRequestError
from app.utils.permissoes import permission_required, login_required
from app.enum.PermissionEnum import PermissionEnum

sensor_service = SensorService()

@login_required
@permission_required(PermissionEnum.SENSOR_CRIAR)
def criar_sensor():
    """
    Cadastra um novo sensor.
    ---
    tags:
      - Sensor
    consumes:
      - application/json
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            id_propriedade:
              type: string
              example: "a1b2c3d4-e5f6-7890-1234-567890abcdef"
            nome:
              type: string
              example: "Sensor de Temperatura 1"
            tanque_id:
              type: string
              example: "f9e8d7c6-b5a4-3210-fedc-ba9876543210"
    responses:
      201:
        description: Sensor cadastrado com sucesso!
      400:
        description: Dados inválidos
      404:
        description: Propriedade ou Tanque não encontrado
      409:
        description: Sensor com o mesmo nome já cadastrado
    """
    data = request.get_json()
    try:
        novo_sensor = sensor_service.criar_sensor(
            propriedade_id=data['id_propriedade'],
            nome=data['nome'],
            tanque_id=data['tanque_id']
        )
        return jsonify({'mensagem': 'Sensor criado com sucesso!', 'sensor': novo_sensor.to_dict()}), 201
    except BadRequestError as e:
        return jsonify({'erro': e.message}), 400
    except NotFoundRequestError as e:
        return jsonify({'erro': e.message}), 404
    except ConflictRequestError as e:
        return jsonify({'erro': e.message}), 409
    except KeyError as e:
        return jsonify({'erro': f'O campo obrigatório "{e}" não foi fornecido'}), 400


@login_required
@permission_required(PermissionEnum.SENSOR_LISTAR)
def listar_sensores():
    """
    Lista todos os sensores cadastrados.
    ---
    tags:
      - Sensor
    responses:
      200:
        description: Lista de sensores
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: string
                example: "uuid-do-sensor"
              nome:
                type: string
                example: "Sensor de Temperatura 1"
              id_propriedade:
                type: string
                example: "uuid-da-propriedade"
              tanque_id:
                type: string
                example: "uuid-do-tanque"
              # Adicione aqui outros campos do sensor
    """
    sensores = sensor_service.listar_sensores()
    return jsonify(sensores), 200

@login_required
@permission_required(PermissionEnum.SENSOR_DETALHAR)
def obter_sensor(sensor_id: str):
    """
    Obtém os detalhes de um sensor específico.
    ---
    tags:
      - Sensor
    parameters:
      - in: path
        name: sensor_id
        required: true
        type: string
        description: ID do sensor a ser detalhado
        example: "uuid-do-sensor"
    responses:
      200:
        description: Detalhes do sensor
        schema:
          type: object
          properties:
            id:
              type: string
              example: "uuid-do-sensor"
            nome:
              type: string
              example: "Sensor de Temperatura 1"
            id_propriedade:
              type: string
              example: "uuid-da-propriedade"
            tanque_id:
              type: string
              example: "uuid-do-tanque"
            # Adicione aqui outros campos do sensor
      404:
        description: Sensor não encontrado
    """
    try:
        sensor = sensor_service.obter_sensor(sensor_id)
        return jsonify(sensor), 200
    except NotFoundRequestError as e:
        return jsonify({'erro': e.message}), 404

@login_required
@permission_required(PermissionEnum.SENSOR_EDITAR)
def atualizar_sensor(sensor_id: str):
    """
    Atualiza os dados de um sensor existente.
    ---
    tags:
      - Sensor
    parameters:
      - in: path
        name: sensor_id
        required: true
        type: string
        description: ID do sensor a ser atualizado
        example: "uuid-do-sensor"
      - in: body
        name: body
        required: false
        schema:
          type: object
          properties:
            id_propriedade:
              type: string
              example: "a1b2c3d4-e5f6-7890-1234-567890abcdef"
            nome:
              type: string
              example: "Novo Nome do Sensor"
            tanque_id:
              type: string
              example: "f9e8d7c6-b5a4-3210-fedc-ba9876543210"
    consumes:
      - application/json
    responses:
      200:
        description: Sensor atualizado com sucesso!
      400:
        description: Dados inválidos
      404:
        description: Sensor ou Propriedade/Tanque não encontrado
      409:
        description: Já existe um sensor com esse nome
    """
    data = request.get_json()
    try:
        sensor_atualizado = sensor_service.atualizar_sensor(
            sensor_id=sensor_id,
            propriedade_id=data.get('id_propriedade'),
            nome=data.get('nome'),
            tanque_id=data.get('tanque_id')
        )
        return jsonify({'mensagem': 'Sensor atualizado com sucesso!', 'sensor': sensor_atualizado.to_dict()}), 200
    except BadRequestError as e:
        return jsonify({'erro': e.message}), 400
    except NotFoundRequestError as e:
        return jsonify({'erro': e.message}), 404
    except ConflictRequestError as e:
        return jsonify({'erro': e.message}), 409

@login_required
@permission_required(PermissionEnum.SENSOR_EXCLUIR)
def deletar_sensor(sensor_id: str):
    """
    Deleta um sensor específico.
    ---
    tags:
      - Sensor
    parameters:
      - in: path
        name: sensor_id
        required: true
        type: string
        description: ID do sensor a ser deletado
        example: "uuid-do-sensor"
    responses:
      200:
        description: Sensor deletado com sucesso!
      404:
        description: Sensor não encontrado
    """
    try:
        sensor_service.deletar_sensor(sensor_id)
        return jsonify({'mensagem': 'Sensor deletado com sucesso!'}), 200
    except NotFoundRequestError as e:
        return jsonify({'erro': e.message}), 404