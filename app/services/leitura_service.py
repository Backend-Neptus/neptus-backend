from app import db
from app.exceptions import BadRequestError, ConflictRequestError, NotFoundRequestError
from app.enum.PermissionEnum import PermissionEnum
from app.models.leitura_model import Leitura
from app.models.usuario_model import Usuario 


class LeituraService:
    def listar_todas_leituras(page, per_page, tanque_id):
        
        #TODO SO PODE RETORNAR AS LEITURAS RELACIONADAS A PROPRIEDADE DO USUARIO LOGADO - IMPLEMENTAR DEPOIS
        if per_page > 50:
            per_page = 50  
        if per_page < 1:
            raise NotFoundRequestError("Itens por página deve ser maior que zero.")

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

    def criar_leitura(usuario_id, tanque_id, turbidez, oxigenio, temperatura, ph, amonia, imagem_cor):
        if not turbidez:
            raise BadRequestError("O campo 'turbidez' deve ser preenchido.")
        if not usuario_id or not tanque_id:
            raise BadRequestError("Os campos 'usuario_id' e 'tanque_id' devem ser preenchidos.")
        
        usuario = Usuario.query.get(usuario_id)
        if not usuario:
            raise NotFoundRequestError("Usuário não encontrado.")

        tanque = Leitura.query.filter_by(tanque=tanque_id).first()
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
