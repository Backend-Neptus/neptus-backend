from app import db
from app.exceptions import BadRequestError, ConflictRequestError, NotFoundRequestError
from app.enum.PermissionEnum import PermissionEnum
from app.utils.permissoes import PermissaoPerfilLocal
from app.models.leitura_model import Leitura 


class LeituraService:
    def listar_todas_leituras(page, per_page):
    
        if per_page > 50:
            per_page = 50
            leituras = Leitura.query.order_by(Leitura.created_at).paginate(
            page=page, per_page=per_page, error_out=False
        )
        else:
            raise NotFoundRequestError("Não foi possível listar leituras.")

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

    def criar_leitura(sensor_id, valor):
        if not valor:
            raise BadRequestError("O campo 'valor' deve ser preenchido.")
        leitura = Leitura(sensor_id=sensor_id, valor=valor)
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
