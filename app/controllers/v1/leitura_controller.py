from flask import request
from app.services.leitura_service import LeituraService
from app.exceptions.app_request_Exception import AppRequestError

class LeituraController:
    def listar_leituras(page=1, per_page=20):
        try:
            return LeituraService.listar_todas_leituras(page, per_page)
        except AppRequestError as e:
            raise e

    def buscar_leitura(leitura_id):
        try:
            return LeituraService.buscar_leitura_por_id(leitura_id)
        except AppRequestError as e:
            raise e
        
    def criar_leitura(valor): # USUARIO ID VAI VIR DO CONTEXTO FLASK (G)
        data = request.get_json()
        try:
            return LeituraService.criar_leitura(valor)
        except AppRequestError as e:
            raise e

    def atualizar_leitura(leitura_id, valor):
        try:
            return LeituraService.atualizar_leitura( leitura_id, valor)
        except AppRequestError as e:
            raise e

    def deletar_leitura(leitura_id):
        try:
            return LeituraService.deletar_leitura(leitura_id)
        except AppRequestError as e:
            raise e
