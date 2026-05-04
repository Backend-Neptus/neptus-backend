from app.utils.permissoes import login_required
from flask import request
from app.services.leitura_service import LeituraService
from app.exceptions.app_request_Exception import AppRequestError

@login_required
def listar_leituras(tanque_id, page=1, per_page=20):
    try:
        return LeituraService.listar_todas_leituras(tanque_id, page, per_page)
    except AppRequestError as e:
        raise e
    
@login_required
def buscar_leitura(leitura_id):
    try:
        return LeituraService.buscar_leitura_por_id(leitura_id)
    except AppRequestError as e:
            raise e
    
@login_required    
def criar_leitura(): # USUARIO ID VAI VIR DO CONTEXTO FLASK (G)
    data = request.get_json()
    tanque_id = data.get('tanque_id')
    turbidez = data.get('turbidez')
    oxigenio = data.get('oxigenio')
    temperatura = data.get('temperatura')
    ph = data.get('ph')
    amonia = data.get('amonia')
    imagem_cor = data.get('imagem_cor')
    try:
        return LeituraService.criar_leitura(tanque_id, turbidez, oxigenio, temperatura, ph, amonia, imagem_cor)
    except AppRequestError as e:
        raise e
    
@login_required
def atualizar_leitura(leitura_id, valor):
    try:
        return LeituraService.atualizar_leitura( leitura_id, valor)
    except AppRequestError as e:
        raise e
    
@login_required
def deletar_leitura(leitura_id):
    try:
        return LeituraService.deletar_leitura(leitura_id)
    except AppRequestError as e:
        raise e
