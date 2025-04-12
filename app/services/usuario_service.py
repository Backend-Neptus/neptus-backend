from flask import request, jsonify
from app import db
from app.models.usuario_model import Usuario
from app.models.perfil_model import Perfil
from app.enum.PermissionEnum import PermissionEnum
from app.exceptions import (BadRequestError, ConflictRequestError,
                            UserDisabledError, GoogleLoginRequestError,
                            NotFoundRequestError, InvalidCredentialsError)
class UsuarioService():
    def registrar_usuario(self, nome: str, email: str, senha: str, perfil_id: int):

        if (not nome) or (not email) or (not senha):
            raise BadRequestError(
                "Os campos 'nome', 'email' e 'senha' devem ser preenchidos")

        if Usuario.query.filter_by(email=email).first():
            raise ConflictRequestError("E-mail ja cadastrado")
        
        perfil = Perfil.query.get(perfil_id)
        if not perfil:
            raise NotFoundRequestError("Perfil nao encontrado")
        
        usuario = Usuario(nome=nome, email=email, perfil_id=perfil.id)
        usuario.set_senha(senha)
        db.session.add(usuario)
        db.session.commit()

        return "Usuário cadastrado com sucesso!"