from app import db
from app.exceptions import BadRequestError, ConflictRequestError, NotFoundRequestError
from app.enum.PermissionEnum import PermissionEnum
from app.exceptions.app_request_Exception import AppRequestError
from app.models.leitura_model import Leitura
from app.models.tanque_model import Tanque
from app.models.usuario_model import Usuario
from flask import g 
from flask import jsonify

class LeituraService:
    def listar_todas_leituras(tanque_id, page, per_page):
        if per_page > 50:
            per_page = 50  


        leituras = Leitura.query.filter(Leitura.tanque == tanque_id).order_by(Leitura.criado_em).paginate(page=page, per_page=per_page, error_out=False)
        return {
            'total': leituras.total,
            'pagina_atual': leituras.page,
            'itens_por_pagina': leituras.per_page,
            'total_paginas': leituras.pages,
            'leituras': [leitura.to_dict() for leitura in leituras]
        }
        

    def buscar_leitura_por_id(leitura_id):
        leitura = Leitura.query.get(leitura_id)
        if not leitura:
            raise NotFoundRequestError("Leitura não encontrada.")
        return leitura.to_dict()

    def criar_leitura(tanque_id, turbidez, oxigenio, temperatura, ph, amonia, cor_agua):
        if not turbidez:
            raise BadRequestError("O campo 'turbidez' deve ser preenchido.")

        usuario_id = str(g.usuario.id)  # pega o usuário autenticado

        if not usuario_id or not tanque_id:
            raise BadRequestError("O campo 'tanque_id' devem ser preenchidos.")
        
        usuario = Usuario.query.get(usuario_id)
        if not usuario:
            raise NotFoundRequestError("Usuário não encontrado.")

        tanque = Tanque.query.get(tanque_id)
        if not tanque:
            raise NotFoundRequestError("Tanque não encontrado.")

        leitura = Leitura(usuario_id=usuario_id, tanque=tanque_id, turbidez=turbidez,
                          oxigenio=oxigenio, temperatura=temperatura,
                          ph=ph, amonia=amonia, cor_agua=cor_agua)
        db.session.add(leitura)
        db.session.commit()
        return leitura.to_dict()

    def atualizar_leitura(leitura_id, valor):
        if not valor:
            raise BadRequestError("O campo 'valor' deve ser preenchido.")

        leitura = Leitura.query.get(leitura_id)
        if not leitura:
            raise NotFoundRequestError("Leitura não encontrada.")
        leitura.valor = valor
        db.session.commit()
        return leitura.to_dict()

    def deletar_leitura(leitura_id):
        leitura = Leitura.query.get(leitura_id)
        if not leitura:
            raise NotFoundRequestError("Leitura não encontrada.")
        db.session.delete(leitura)
        db.session.commit()


    def criar_leituras_em_lote(lote):
        if not isinstance(lote, list):
            raise BadRequestError("O corpo da requisição deve ser uma lista de leituras.")

        usuario_id = str(g.usuario.id)
        if not usuario_id:
            raise BadRequestError("Usuário não autenticado.")


        usuario = Usuario.query.get(usuario_id)
        if not usuario:
            raise NotFoundRequestError("Usuário não encontrado.")


        tanques_ids = {leitura_data.get('tanque_id') for leitura_data in lote}
        tanques_validos = {t.id: t for t in Tanque.query.filter(Tanque.id.in_(tanques_ids)).all()}

        leituras_criadas = []
        leituras_erradas = []

        for leitura_data in lote:
            tanque_id = leitura_data.get('tanque_id')
            turbidez = leitura_data.get('turbidez')
            oxigenio = leitura_data.get('oxigenio')
            temperatura = leitura_data.get('temperatura')
            ph = leitura_data.get('ph')
            amonia = leitura_data.get('amonia')
            cor_agua = leitura_data.get('cor_agua')

            try:
                if not turbidez:
                    raise BadRequestError("O campo 'turbidez' deve ser preenchido.")
                if not tanque_id or tanque_id not in tanques_validos:
                    raise NotFoundRequestError("Tanque não encontrado.")
                if cor_agua is None or cor_agua < 1 or cor_agua > 5:
                    raise BadRequestError("O campo 'cor_agua' deve ser um inteiro entre 1 e 5.")

                leitura = Leitura(
                    usuario_id=usuario_id, 
                    tanque=tanque_id, 
                    turbidez=turbidez,
                    oxigenio=oxigenio, 
                    temperatura=temperatura,
                    ph=ph, 
                    amonia=amonia, 
                    cor_agua=cor_agua
                )
                db.session.add(leitura)
                leituras_criadas.append(leitura)

            except (BadRequestError, NotFoundRequestError) as e:
                leitura_dict = {
                    "tanque_id": tanque_id, 
                    "turbidez": turbidez,
                    "oxigenio": oxigenio,
                    "temperatura": temperatura,
                    "ph": ph,
                    "amonia": amonia,
                    "cor_agua": cor_agua,
                    "erro": str(e)
                }
                leituras_erradas.append(leitura_dict)

        if leituras_criadas:
            db.session.commit()

        if leituras_erradas:
            return jsonify({
                "code": "ConflictRequestError",
                "message": "Falha parcial. Alguns registros corromperam validation.",
                "status": 409,
                "leituras_erradas": leituras_erradas
            }), 409

        return jsonify({
            "code": "Success",
            "message": "Leituras criadas com sucesso.",
            "status": 201
        }), 201