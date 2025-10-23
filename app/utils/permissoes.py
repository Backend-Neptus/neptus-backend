from functools import wraps
from flask_jwt_extended import jwt_required, get_jwt_identity, verify_jwt_in_request
from flask import g, jsonify, request
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
                # Isso jamais deve acontecer, mas é uma boa prática
                    # Esperamos que o usuário tenha um perfil associado
                        # Espero que isso jamais aconteça
                            # Espero que o usuário tenha um perfil associado
                        # Isso deve ser tratado em outro lugar
                # verificar se o usuário está logado e tem um perfil associado
                raise UnauthorizedRequestError("Usuário não encontrado ou sem perfil associado")
            permissoes_lista = usuario.perfil.permissoes
            # Permitir acesso total para administradores
            if usuario.e_admin:
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
                raise UnauthorizedRequestError("Você não possui permissão para acessar esta funcionalidade!")
            if not usuario.esta_ativo:
                raise UnauthorizedRequestError("Usuário inativo, favor entrar em contato com o administrador do sistema")
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
            ip_address = request.headers.get('X-Forwarded-For', request.remote_addr)
            g.user_ip = ip_address
            print(f"IP do usuário: {g.user_ip}")
            return g.usuario
        else:
            g.usuario = None
    except Exception as e:
        g.usuario = None