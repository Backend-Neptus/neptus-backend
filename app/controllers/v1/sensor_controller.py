'''Recebe as requisições do cliente (geralmente via HTTP) e passa os dados para o Service. Depois, devolve a resposta ao cliente.
Exemplo: Um endpoint POST /usuarios que chama o serviço para criar um novo usuário.

Cliente -> Controller -> Service -> Model -> Banco
'''

from flask import request, jsonify
from app import db
from app.models.sensor_model import Sensor
from app.exceptions.app_request_Exception import AppRequestError
from app.services.sensor_service import Sensorservice
from app.enum.PermissionEnum import PermissionEnum
from app.utils.permissoes import login_required, permission_required, PermissaoPerfilLocal

@login_required
@permission_required(PermissionEnum.SENSOR_CRIAR)
def registrar_sensor():
    if not request.is_json:
        return jsonify({'erro': 'Requisição deve ser JSON'}), 400
    
    data = request.get_json()
    nome = data.get('nome')
    sensor_id = data.get('id')

    if not nome or not sensor_id:
        return jsonify({'erro': 'Nome e ID são obrigatórios'}), 400
    
    try:
        sensor_data = Sensorservice().criar_sensor(sensor_id, nome)
        return jsonify({
            'mensagem': 'Sensor criado com sucesso',
            'sensor': sensor_data
        }), 200
    except AppRequestError as e:
        return jsonify(e.to_dict()), e.status_code
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

@login_required
@permission_required(PermissionEnum.SENSOR_DETALHAR)    
def buscar_sensor():
    sensor_id = request.args.get('id')
    nome = request.args.get('nome')
    
       
    if not sensor_id and not nome:
        return jsonify({'erro': 'Forneça id ou nome para busca'}), 400
    
    try:
        sensor_data = Sensorservice().chamar_id_sensor(sensor_id, nome)
        if not sensor_data:
            return jsonify({'erro': 'Sensor não encontrado'}), 404
        return jsonify(sensor_data), 200
    except AppRequestError as e:
        return jsonify(e.to_dict()), e.status_code
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

@login_required
@permission_required(PermissionEnum.SENSOR_LISTAR)
def listar_sensores():
    if not request.is_json:
        return jsonify({'erro': 'Requisição deve ser JSON'}), 400

    data = request.get_json()
    nome = request.args.get('nome')
    propriedade_id = request.args.get('propriedade_id') 
    
    try:
        sensor_data = Sensorservice().listar_todos_sensores(propriedade_id, nome)
        return jsonify({
        'mensagem': 'Sensores chamados com sucesso',
        'sensor': sensor_data
        }), 200
    except AppRequestError as e:
        return jsonify(e.to_dict()), e.status_code

@login_required
@permission_required(PermissionEnum.SENSOR_EDITAR)
def atualizar_sensor(sensor_id):
    if not request.is_json:
        return jsonify({'erro': 'Requisição deve ser JSON'}), 400
    
    data = request.get_json()
    nome = data.get('nome')
    sensor_id = data.get('id')

    if not sensor_id or not nome:
        return jsonify({'erro': 'ID e nome são obrigatórios'}), 400
    
    try:  
        resultado = Sensorservice().atualizar_sensor(id=sensor_id, nome=nome)
        return jsonify({
            'mensagem': 'Sensor atualizado com sucesso',
            'dados': resultado  # Inclui os dados retornados pelo serviço
        }), 200
    except AppRequestError as e:
        return jsonify(e.to_dict()), e.status_code
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

@login_required
@permission_required(PermissionEnum.SENSOR_EXCLUIR)
def excluir_sensor(sensor_id):
    if not request.is_json:
        return jsonify({'erro': 'Requisição deve ser JSON'}), 400

    try:
        Sensorservice().deletar_sensor(sensor_id)  # Só precisa do ID
        return jsonify({
            'mensagem': 'Sensor excluído com sucesso',
            'id': sensor_id  # Boa prática retornar o ID excluído
        }), 200
    
    except AppRequestError as e:
        return jsonify(e.to_dict()), e.status_code
    except Exception as e:
        # Em produção, logar o erro (ex: logging.error(e))
        return jsonify({
            'erro': 'Falha ao excluir sensor',
            'detalhes': str(e)
        }), 500