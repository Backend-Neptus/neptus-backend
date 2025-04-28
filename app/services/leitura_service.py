from app import db
from app.models import Leitura, Tanque, Propriedade
from app.exceptions import NotFoundRequestError, BadRequestError
from flask import g  # Importe o g


class LeituraService:
    def criar_leitura(self, id_propriedade, id_tanque, valor, cor_agua, oxigenio, temperatura, ph_agua, amonia): # Parâmetros adicionais
        usuario_request = g.usuario  # Obtenha o usuário do g
        if not usuario_request:
            raise NotFoundRequestError("Usuário não autenticado")
        tanque = Tanque.query.filter_by(id=id_tanque).first()
        if not tanque:
            raise BadRequestError("Tanque não encontrado")
        propriedade = Propriedade.query.filter_by(id=id_propriedade).first()
        if not propriedade:
            raise BadRequestError("Propriedade não encontrada")
        
        try:
            cor_agua = int(cor_agua)
            oxigenio = float(oxigenio)
            temperatura = float(temperatura)
            ph_agua = float(ph_agua)
            amonia = float(amonia)
        except ValueError:
            raise BadRequestError("Um ou mais valores de entrada são inválidos.")

        if not 1 <= cor_agua <= 10: # (ajuste os limites conforme necessário)
            raise BadRequestError("Valor de cor_agua inválido. Deve estar entre 1 e 10.")
        if not 0 <= oxigenio <= 15:
            raise BadRequestError("Valor de oxigenio inválido. Deve estar entre 0 e 15.")
        if not 10 <= temperatura <= 40:
            raise BadRequestError("Valor de temperatura inválido. Deve estar entre 10 e 40.")
        if not 0 <= ph_agua <= 14:
            raise BadRequestError("Valor de ph_agua inválido. Deve estar entre 0 e 14.")
        if not 0 <= amonia <= 5:
            raise BadRequestError("Valor de amonia inválido. Deve estar entre 0 e 5.")

        nova_leitura = Leitura(
            valor=valor,
            cor_agua=cor_agua,          
            oxigenio=oxigenio,
            temperatura=temperatura,
            ph_agua=ph_agua,
            amonia=amonia,
            id_usuario=usuario_request.id,
            id_tanque=id_tanque,
            id_propriedade=id_propriedade,
            propriedade=propriedade,
            tanque=tanque,
        )
        db.session.add(nova_leitura)
        db.session.commit()
        return nova_leitura

    def listar_leituras(self):
        leituras = [leitura.to_dict() for leitura in Leitura.query.all()]
        return leituras

    def obter_leitura(self, id):
        leitura = self._get_leitura_or_404(id)
        return leitura.to_dict()

    def atualizar_leitura(self, id, id_tanque=None, cor_agua=None, oxigenio=None, temperatura=None, ph_agua=None, amonia=None):
        leitura = self._get_leitura_or_404(id)

        if id_tanque is None and cor_agua is None and oxigenio is None and temperatura is None and ph_agua is None and amonia is None:
            raise BadRequestError("Nenhum dado válido fornecido para atualização (além de valor).")

        if id_tanque is not None:
            tanque = Tanque.query.get(id_tanque)
            if not tanque:
                raise BadRequestError("Tanque não encontrado")
            leitura.id_tanque = id_tanque
        if cor_agua is not None:
            try:
                cor_agua = int(cor_agua)
                if not 1 <= cor_agua <= 10:
                    raise BadRequestError("Valor de cor_agua inválido. Deve estar entre 1 e 10.")
                leitura.cor_agua = cor_agua
            except (ValueError, TypeError):
                raise BadRequestError("Valor de cor_agua inválido.")
        if oxigenio is not None:
            try:
                oxigenio = float(oxigenio)
                if not 0 <= oxigenio <= 15:
                    raise BadRequestError("Valor de oxigenio inválido. Deve estar entre 0 e 15.")
                leitura.oxigenio = oxigenio
            except (ValueError, TypeError):
                raise BadRequestError("Valor de oxigenio inválido.")
        if temperatura is not None:
            try:
                temperatura = float(temperatura)
                if not 10 <= temperatura <= 40:
                    raise BadRequestError("Valor de temperatura inválido. Deve estar entre 10 e 40.")
                leitura.temperatura = temperatura
            except (ValueError, TypeError):
                raise BadRequestError("Valor de temperatura inválido.")
        if ph_agua is not None:
            try:
                ph_agua = float(ph_agua)
                if not 0 <= ph_agua <= 14:
                    raise BadRequestError("Valor de ph_agua inválido. Deve estar entre 0 e 14.")
                leitura.ph_agua = ph_agua
            except (ValueError, TypeError):
                raise BadRequestError("Valor de ph_agua inválido.")
        if amonia is not None:
            try:
                amonia = float(amonia)
                if not 0 <= amonia <= 5:
                    raise BadRequestError("Valor de amonia inválido. Deve estar entre 0 e 5.")
                leitura.amonia = amonia
            except (ValueError, TypeError):
                raise BadRequestError("Valor de amonia inválido.")

        db.session.commit()
        return leitura

    def _get_leitura_or_404(self, id):
        leitura = Leitura.query.get(id)
        if not leitura:
            raise NotFoundRequestError("Leitura não encontrada")
        return leitura

    def deletar_leitura(self, id):
        db.session.delete(self._get_leitura_or_404(id))
        db.session.commit()