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

    def criar_leitura(tanque_id, turbidez, oxigenio, temperatura, ph, amonia, imagem_cor):
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
                          ph=ph, amonia=amonia, imagem_cor=imagem_cor)
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

        leituras_criadas = []
        leituras_erradas = []

        for leitura_data in lote:
            tanque_id = leitura_data.get('tanque_id')
            turbidez = leitura_data.get('turbidez')
            oxigenio = leitura_data.get('oxigenio')
            temperatura = leitura_data.get('temperatura')
            ph = leitura_data.get('ph')
            amonia = leitura_data.get('amonia')
            imagem_cor = leitura_data.get('imagem_cor')

            try:
                leitura = LeituraService.criar_leitura(
                tanque_id, turbidez, oxigenio, temperatura, ph, amonia, imagem_cor
            )
            except:
                leitura = {"tanque_id": tanque_id, 
                           "turbidez": turbidez,
                            "oxigenio": oxigenio,
                            "temperatura": temperatura,
                            "ph": ph,
                            "amonia": amonia,
                            "imagem_cor": imagem_cor
                           }

                leituras_erradas.append(leitura)
                continue
            leituras_criadas.append(leitura)

        db.session.commit()
        if leituras_erradas:
            # Caso existam tanques inválidos
            return jsonify({
                "code": "ConflictRequestError",
                "message": "Falha ao criar leituras, alguns tanques são inválidos.",
                "status": 409,
                "leituras_erradas": leituras_erradas
            }), 409

        # Caso tudo tenha dado certo
        return jsonify({
            "code": "Success",
            "message": "Leituras criadas com sucesso.",
            "status": 201
        }), 201