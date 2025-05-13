from flask import g
from app.enum.PermissionEnum import PermissionEnum
from app.exceptions.bad_request_error import BadRequestError
from app.exceptions.not_found_request_error import NotFoundRequestError
from app.models.perfil_model import Perfil
from app.models.propriedade_model import Propriedade
from app.models.utils.associacoes import propriedade_usuarios, propriedade_perfil
from app import db
from sqlalchemy import select, join, update


class PermissaoPerfilLocal:
    def __init__(self):
        self.perfil_local = None
        
    @staticmethod
    def __get_perfil_local_usuario(usuario_id, propriedade_id):
        stmt = select(propriedade_usuarios.c.perfil_local).where(
            propriedade_usuarios.c.usuario_id == usuario_id,
            propriedade_usuarios.c.propriedade_id == propriedade_id)
        result = db.session.execute(stmt).scalar()
        return result

    def verificar_permissao_perfil_local(self, permissao: PermissionEnum, propriedade_id):
        if not permissao:
            raise NotFoundRequestError("Permissão não encontrada ou inexistente")
        usuario_request = g.usuario
        propriedade = propriedade = Propriedade.query.get(propriedade_id)
        if not propriedade:
            raise NotFoundRequestError("Propriedade não encontrada")
        if usuario_request.is_admin:
            return True
        if propriedade.proprietario_id == usuario_request.id:
            return True
        perfil_id = self.__get_perfil_local_usuario(usuario_request.id, propriedade_id)
        perfil = Perfil.query.filter_by(id=perfil_id).first()
        if not perfil:
            raise NotFoundRequestError("Você não possui permissão para essa ação")
        if permissao.value not in perfil.permissoes:
            raise NotFoundRequestError("Você não possui permissão para essa ação")
        return True



    def atualizar_perfil_local(self, usuario_id, propriedade_id, novo_perfil_id):
        """
        Atualiza o perfil local de um usuario em uma propriedade.
        NÃO USAR ESSE METODO SEM ANTES VERIFICAR EXISTENCIA DO USUARIO, PERFIL E PROPRIEDADE
        METODO UTILIZADO APOS VERIFICAR_PERMISSAO_PERFIL_LOCAL

        :param usuario_id: O id do usuario
        :param propriedade_id: O id da propriedade
        :param novo_perfil_id: O id do perfil local a ser atualizado
        :raises BadRequestError: Se o usuario nao estiver cadastrado na propriedade
        :return: None
        """
        stmt = update(propriedade_usuarios).where(
            propriedade_usuarios.c.usuario_id == usuario_id,
            propriedade_usuarios.c.propriedade_id == propriedade_id
        ).values(perfil_local=novo_perfil_id)
        resultado = db.session.execute(stmt)
        if resultado.rowcount == 0:
            raise BadRequestError("Usuario não cadastrado na propriedade")
        db.session.commit()