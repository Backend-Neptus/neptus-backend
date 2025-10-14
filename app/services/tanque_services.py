from flask import g
from app import db
from app.models.tanque_model import Tanque
from app.models.propriedade_model import Propriedade
from app.exceptions import BadRequestError, ConflictRequestError, NotFoundRequestError


class TanqueService:

    def cadastrar_tanque(
        self,
        nome: str,
        id_propriedade: str,
        area_tanque: float,
        tipo_peixe: str,
        peso_peixe: float = None,
        qtd_peixe: int = None
    ):
        """Cadastra um novo tanque vinculado ao usuário logado e à propriedade informada."""
        id_usuario = str(g.usuario.id)  # pega o usuário autenticado
        self.__verificar_dados(nome, area_tanque, tipo_peixe)

        # Verifica duplicidade de nome (pode limitar à propriedade, se quiser)
        tanque_existente = Tanque.query.filter_by(nome=nome).first()
        if tanque_existente:
            raise ConflictRequestError("Já existe um tanque com este nome.")

        # Verifica se a propriedade existe
        propriedade = Propriedade.query.get(id_propriedade)
        if not propriedade:
            raise NotFoundRequestError("Propriedade não encontrada.")

        # Cria o tanque
        novo_tanque = Tanque(
            nome=nome,
            id_usuario=id_usuario,
            id_propriedade=id_propriedade,
            area_tanque=area_tanque,
            tipo_peixe=tipo_peixe,
            peso_peixe=peso_peixe,
            qtd_peixe=qtd_peixe,
            ativo=True
        )

        db.session.add(novo_tanque)
        db.session.commit()

        return novo_tanque.to_dict()
    
    def listar_tanques(self, page, per_page):
        """Lista todos os tanques com paginação."""
        if per_page > 50:
            per_page = 50

        tanques = Tanque.query.order_by(Tanque.criado_em)\
            .paginate(page=page, per_page=per_page, error_out=False)

        return {
            'total': tanques.total,
            'pagina_atual': tanques.page,
            'itens_por_pagina': tanques.per_page,
            'total_paginas': tanques.pages,
            'tanques': [tanque.to_dict() for tanque in tanques.items]
        }
    
    def exibir_tanque(self, id_tanque):
        """
        Retorna os dados de um tanque específico para edição.
        O front-end pode usar esses dados para preencher o formulário.
        """
        tanque = Tanque.query.get(id_tanque)
        if not tanque:
            raise NotFoundRequestError("Tanque não encontrado.")
        
        # Retorna apenas os campos que podem ser editados
        return {
            "nome": tanque.nome,
            "area_tanque": tanque.area_tanque,
            "tipo_peixe": tanque.tipo_peixe,
            "peso_peixe": tanque.peso_peixe,
            "qtd_peixe": tanque.qtd_peixe,
            "ativo": tanque.ativo
        }
    
    def atualizar_tanque(self, id_tanque, dados: dict):
        """Atualiza os dados de um tanque existente."""
        
        # Busca o tanque pelo ID
        tanque = Tanque.query.get(id_tanque)
        if not tanque:
            raise NotFoundRequestError("Tanque não encontrado.")

        # Campos permitidos para atualização
        campos_permitidos = ['nome', 'area_tanque', 'tipo_peixe', 'peso_peixe', 'qtd_peixe', 'ativo']

        for campo in campos_permitidos:
            if campo in dados:
                valor = dados[campo]
                # Validações básicas
                if campo == 'nome' and (not valor or not valor.strip()):
                    raise BadRequestError("O nome do tanque não pode ser vazio.")
                if campo == 'area_tanque' and (not valor or valor <= 0):
                    raise BadRequestError("A área do tanque deve ser maior que zero.")
                if campo == 'tipo_peixe' and (not valor or not valor.strip()):
                    raise BadRequestError("O tipo de peixe é obrigatório.")

                setattr(tanque, campo, valor)

        db.session.commit()
        return tanque.to_dict()
    
    def desativar_tanque(self, id_tanque):
        """
        Desativa um tanque existente, marcando 'ativo' como False.
        """
        tanque = Tanque.query.get(id_tanque)
        if not tanque:
            raise NotFoundRequestError("Tanque não encontrado.")

        tanque.ativo = False
        db.session.commit()
        return tanque.to_dict()

    # ---------------- MÉTODOS PRIVADOS ---------------- #

    def __verificar_dados(self, nome, area_tanque, tipo_peixe):
        """Valida campos obrigatórios e tipos básicos."""
        if not nome or not nome.strip():
            raise BadRequestError("O nome do tanque é obrigatório.")
        if not area_tanque or area_tanque <= 0:
            raise BadRequestError("A área do tanque deve ser maior que zero.")
        if not tipo_peixe or not tipo_peixe.strip():
            raise BadRequestError("O tipo de peixe é obrigatório.")
