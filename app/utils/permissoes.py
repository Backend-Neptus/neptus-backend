from functools import wraps
from flask_jwt_extended import jwt_required, get_jwt_identity, verify_jwt_in_request
from flask import jsonify
from app.models.usuario_model import Usuario 

def permission_required(permissao):
    def wrapper(func):
        @wraps(func)
        @jwt_required()
        def decorator(*args, **kwargs):
            usuario_id = get_jwt_identity()
            usuario = Usuario.query.get(usuario_id)

            if not usuario or not usuario.perfil:
                return jsonify({'erro': 'Usuário sem perfil'}), 403
            permissoes_lista = usuario.perfil.permissoes

            # Permitir acesso total para administradores
            if usuario.is_admin:
                return func(*args, **kwargs)

            if permissao.value not in permissoes_lista:
                return jsonify({'erro': 'Permissão negada'}), 403

            return func(*args, **kwargs)
        return decorator
    return wrapper

def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            verify_jwt_in_request()
            usuario_id = get_jwt_identity()
            usuario = Usuario.query.get(usuario_id)

            if not usuario:
                return jsonify({'erro': 'Usuário não encontrado'}), 404
            if not usuario.is_active:
                return jsonify({'erro': 'Seu usuário foi desativado'}), 401

            return func(*args, **kwargs)
        except Exception as e:
            return jsonify({'erro': 'Token inválido ou ausente'}), 401

    return wrapper