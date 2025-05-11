from functools import wraps
from flask_jwt_extended import jwt_required, get_jwt_identity, verify_jwt_in_request
from flask import g, jsonify
from app.exceptions.unauthorized_request_error import UnauthorizedRequestError
from app.exceptions.app_request_Exception import AppRequestError
from app.models.usuario_model import Usuario 

def permission_required(permissao):
    def wrapper(func):
        @wraps(func)
        @jwt_required()
        def decorator(*args, **kwargs):
            usuario = g.usuario

            if not usuario or not usuario.perfil:
                return jsonify({'erro': 'Usuário sem perfil'}), 403
            permissoes_lista = usuario.perfil.permissoes

            # Permitir acesso total para administradores
            if usuario.is_admin:
                return func(*args, **kwargs)

            if permissao.value not in permissoes_lista:
                raise UnauthorizedRequestError("Você não possui permissão para acessar esta funcionalidade!")

            return func(*args, **kwargs)
        return decorator
    return wrapper

def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            usuario = carregar_usuario_logado()

            if not usuario:
                return jsonify({'erro': 'Usuário não encontrado, logue novamente'}), 404
            if not usuario.is_active:
                return jsonify({'erro': 'Seu usuário foi desativado'}), 401

            return func(*args, **kwargs)
        except AppRequestError as e:
            return jsonify(e.to_dict()), e.status_code

    return wrapper

def carregar_usuario_logado():
    try:
        verify_jwt_in_request(optional=True)
        usuario_id = get_jwt_identity()
        if usuario_id:
            g.usuario = Usuario.query.get(usuario_id)
            return g.usuario
            
        else:
            g.usuario = None
    except Exception as e:
        g.usuario = None