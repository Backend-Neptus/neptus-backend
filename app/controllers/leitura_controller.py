from flask import request, jsonify
from app.exceptions import BadRequestError, NotFoundRequestError
from app.utils.permissoes import permission_required, login_required
from app.enum.PermissionEnum import PermissionEnum
from app.services.leitura_service import LeituraService

@login_required
@permission_required(PermissionEnum.LEITURA_CRIAR)
def criar_leitura():
    """
    Cria uma nova leitura.
    ---
    tags:
      - Leitura
    consumes:
      - application/json
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - valor
            - id_Tanque
            - id_propriedade
            - cor_agua
            - oxigenio
            - temperatura
            - ph_agua
            - amonia
          properties:
            valor:
              type: string  # Ou number
              example: "25.5"
            id_Tanque:
              type: string
              example: "..."
            id_propriedade:
              type: string
              example: "..."
            cor_agua:
              type: integer  # Correção no Swagger
              example: 1
            oxigenio:
              type: number
              example: 7.8
            temperatura:
              type: number
              example: 28.2
            ph_agua:
              type: number
              example: 6.5
            amonia:
              type: number
              example: 0.1
    responses:
      201:
        description: Leitura criada com sucesso
      400:
        description: Dados inválidos
      401:
        description: Usuário não autenticado
    """
    data = request.get_json()
    id_propriedade = data.get('id_propriedade')
    id_tanque = data.get('id_tanque')
    valor = data.get('valor')
    try:
        cor_agua = int(data.get('cor_agua'))
        oxigenio = float(data.get('oxigenio'))
        temperatura = float(data.get('temperatura'))
        ph_agua = float(data.get('ph_agua'))
        amonia = float(data.get('amonia'))
    except (ValueError, TypeError):
        return jsonify({'erro': 'Tipos de dados inválidos nos parâmetros de entrada.'}), 400

    try:
        return jsonify({'mensagem': 'Leitura criada com sucesso', 'leitura': LeituraService().criar_leitura(id_propriedade, id_tanque, valor, cor_agua, oxigenio, temperatura, ph_agua, amonia).to_dict()}), 201
    except BadRequestError as e:
        return jsonify({'erro': e.message}), 400
    except NotFoundRequestError as e:
        return jsonify({'erro': e.message}), 401
    
@login_required
@permission_required(PermissionEnum.LEITURA_LISTAR)
def listar_leituras():
    """
    Lista todas as leituras.
    ---
    tags:
      - Leitura
    responses:
      200:
        description: Lista de leituras
    """
    leituras = LeituraService().listar_leituras()
    return jsonify(leituras), 200

@login_required
@permission_required(PermissionEnum.LEITURA_LISTAR)
def listar_leituras():
    """
    Lista todas as leituras.
    ---
    tags:
      - Leitura
    responses:
      200:
        description: Lista de leituras
    """
    leituras = LeituraService().listar_leituras()
    return jsonify(leituras), 200

@login_required
@permission_required(PermissionEnum.LEITURA_DETALHAR)
def detalhar_leitura(id):
    """
    Obtém uma leitura específica.
    ---
    tags:
      - Leitura
    parameters:
      - in: path
        name: id
        required: true
        type: string
        description: ID da leitura
    responses:
      200:
        description: Detalhes da leitura
      404:
        description: Leitura não encontrada
    """
    leitura = LeituraService().obter_leitura(id)
    return jsonify(leitura), 200



@login_required
@permission_required(PermissionEnum.LEITURA_EXCLUIR)
def deletar_leitura(id):
    """
    Deleta uma leitura.
    ---
    tags:
      - Leitura
    parameters:
      - in: path
        name: id
        required: true
        type: string
        description: ID da leitura a ser deletada
    responses:
      200:
        description: Leitura deletada com sucesso
      404:
        description: Leitura não encontrada
    """
    try:
        
        LeituraService().deletar_leitura(id)
        return jsonify({'mensagem': 'Leitura deletada com sucesso'}), 200
    except NotFoundRequestError as e:
        return jsonify({'erro': e.message}), 404
    

@login_required
@permission_required(PermissionEnum.LEITURA_EDITAR)
def atualizar_leitura(id):
    """
    Atualiza uma leitura existente.
    ---
    tags:
      - Leitura
    parameters:
      - in: path
        name: id
        required: true
        type: string
        description: ID da leitura a ser atualizada
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            id_tanque:
              type: string
              example: "novo_id_do_tanque"
            cor_agua:
              type: integer
              example: 2
            oxigenio:
              type: number
              example: 8.0
            temperatura:
              type: number
              example: 29.0
            ph_agua:
              type: number
              example: 7.0
            amonia:
              type: number
              example: 0.2
    responses:
      200:
        description: Leitura atualizada com sucesso
      400:
        description: Dados inválidos
      404:
        description: Leitura não encontrada
    """
    data = request.get_json()
    mensagem_adicional = []
    if 'valor' in data:
        mensagem_adicional.append("O campo 'valor' não pode ser atualizado e foi ignorado.")

    dados_atualizacao = {}
    if 'id_tanque' in data:
        dados_atualizacao['id_tanque'] = data['id_tanque']
    if 'cor_agua' in data:
        dados_atualizacao['cor_agua'] = data['cor_agua']
    if 'oxigenio' in data:
        dados_atualizacao['oxigenio'] = data['oxigenio']
    if 'temperatura' in data:
        dados_atualizacao['temperatura'] = data['temperatura']
    if 'ph_agua' in data:
        dados_atualizacao['ph_agua'] = data['ph_agua']
    if 'amonia' in data:
        dados_atualizacao['amonia'] = data['amonia']

    try:
        leitura_atualizada = LeituraService().atualizar_leitura(id, **dados_atualizacao)
        mensagem = {'mensagem': 'Leitura atualizada com sucesso', 'data': leitura_atualizada.to_dict()}
        if mensagem_adicional:
            mensagem['informacao'] = mensagem_adicional
        return jsonify(mensagem), 200
    except NotFoundRequestError as e:
        return jsonify({'erro': e.message}), 404
    except BadRequestError as e:
        return jsonify({'erro': e.message}), 400