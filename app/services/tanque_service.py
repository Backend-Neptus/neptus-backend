from app import db
from app.models.tanque_model import Tanque
from app.models.propriedade_model import Propriedade
from app.exceptions import BadRequestError, NotFoundRequestError, ConflictRequestError
from flask import g # Importe o g

class TanqueService:

    def cadastrar_tanque(self, nome: str, propriedade_id: str):
        if not nome or not propriedade_id:
            raise BadRequestError("Os campos 'nome' e 'propriedade_id' são obrigatórios")

        propriedade = Propriedade.query.get(propriedade_id) # Verificar se a propriedade existe
        if not propriedade:
            raise NotFoundRequestError("Propriedade não encontrada")

        usuario_request = g.usuario
        if not usuario_request:
            raise NotFoundRequestError("Token invalido.")
        
        if Tanque.query.filter_by(nome=nome, propriedade_id=propriedade_id).first(): # Verificar se já existe um tanque com o mesmo nome nesta propriedade
            raise ConflictRequestError("Já existe um tanque com este nome nesta propriedade")

        novo_tanque = Tanque(nome=nome, propriedade=propriedade, propriedade_id=propriedade_id, usuario=usuario_request, usuario_id=usuario_request.id ) # Usando o relacionamento
        db.session.add(novo_tanque)
        db.session.commit()

        return novo_tanque

    def listar_tanques(self):
        return Tanque.query.all()

    def detalhar_tanque(self, id: str):
        tanque = Tanque.query.get(id)
        if not tanque:
            raise NotFoundRequestError("Tanque não encontrado")
        return tanque

    def atualizar_tanque(self, id: str, nome: str, propriedade_id: str, status: str):
        if not nome or not propriedade_id or not status:
            raise BadRequestError("Os campos 'nome', 'propriedade_id' e 'status' são obrigatórios")

        tanque = Tanque.query.get(id)
        if not tanque:
            raise NotFoundRequestError("Tanque não encontrado")

        propriedade = Propriedade.query.get(propriedade_id) # Verificar se a propriedade existe
        if not propriedade:
            raise NotFoundRequestError("Propriedade não encontrada")

        tanque_com_mesmo_nome = Tanque.query.filter(Tanque.nome == nome, Tanque.propriedade_id == propriedade_id, Tanque.id != id).first() # Verificar se já existe um tanque com o mesmo nome (excluindo o tanque atual)
        if tanque_com_mesmo_nome:
            raise ConflictRequestError("Já existe um tanque com este nome nesta propriedade")

        tanque.nome = nome
        tanque.propriedade = propriedade  # Usando o relacionamento
        tanque.status = status
        db.session.commit()

        return tanque

    def deletar_tanque(self, id: str):
        tanque = Tanque.query.get(id)
        if not tanque:
            raise NotFoundRequestError("Tanque não encontrado")

        db.session.delete(tanque)
        db.session.commit()