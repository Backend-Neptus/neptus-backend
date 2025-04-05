from flask import request, jsonify
from flask_jwt_extended import create_access_token
from app import db
from app.models.usuario_model import Usuario

def login():
    data = request.get_json()
    email = data.get('email')
    senha = data.get('senha')

    usuario = Usuario.query.filter_by(email=email).first()
    if usuario and usuario.verificar_senha(senha):
        access_token = create_access_token(identity=str(usuario.id))
        return jsonify({'token': access_token}), 200

    return jsonify({'erro': 'Email ou senha inválidos'}), 401