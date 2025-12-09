from functools import wraps
from flask_jwt_extended import jwt_required, get_jwt_identity, verify_jwt_in_request
from flask import g, jsonify, request
from app.exceptions.unauthorized_request_error import UnauthorizedRequestError
from app.exceptions.app_request_Exception import AppRequestError
from app.models.usuario_model import Usuario 

def permission_required(permissao):
    def wrapper(func):
        @wraps(func)
        def decorator(*args, **kwargs):
            usuario = g.get("usuario")
            if not usuario:
                raise UnauthorizedRequestError("Usuário não carregado — coloque @login_required acima de @permission_required")
            if usuario.e_admin is True:  # ← Comparação explícita
                return func(*args, **kwargs)
            if not usuario.perfil:
                raise UnauthorizedRequestError("Usuário sem perfil definido!")
            permissoes_lista = usuario.perfil.permissoes
            if permissao.value not in permissoes_lista: 
                raise UnauthorizedRequestError("Você não possui permissão para acessar esta funcionalidade!")
            return func(*args, **kwargs)
        return decorator
    return wrapper

def login_required(func):
    @wraps(func)
    @jwt_required()
    def wrapper(*args, **kwargs):
        try:
            usuario = carregar_usuario_logado()
            if not usuario: 
                raise UnauthorizedRequestError("Você não possui permissão para acessar esta funcionalidade!")
            g.usuario = usuario 
            if not usuario.esta_ativo:
                raise UnauthorizedRequestError("Usuário inativo, favor entrar em contato com o administrador do sistema")
            return func(*args, **kwargs)
        except AppRequestError as e:
            return jsonify(e.to_dict()), e.status_code
    return wrapper

def carregar_usuario_logado():
    usuario_id = get_jwt_identity()
    if usuario_id:
        g.usuario = Usuario.query.get(usuario_id)
        g.user_ip = request.headers.get('X-Forwarded-For', request.remote_addr)
        return g.usuario
    g.usuario = None
    return None