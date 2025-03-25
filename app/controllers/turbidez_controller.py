from flask import request, jsonify
from app import db
from app.models.turbidez_model import Turbidez

def salvar_turbidez():
    data = request.get_json()

    if 'turbidez' not in data:
        return jsonify({"erro": "Campo 'turbidez' é obrigatório"}), 400

    nova_leitura = Turbidez(valor=data['turbidez'])
    db.session.add(nova_leitura)
    db.session.commit()

    return jsonify({"mensagem": "Leitura salva com sucesso!"}), 201
