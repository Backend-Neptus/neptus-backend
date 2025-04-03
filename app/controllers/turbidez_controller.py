from flask import request, jsonify
from app import db
from app.models.turbidez_model import Turbidez

def salvar_turbidez():
    
    """
    Salva uma nova leitura de turbidez.
    ---
    tags:
      - Turbidez
    consumes:
      - application/json
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            turbidez:
              type: string
              example: "45.3"
    responses:
      201:
        description: Leitura salva com sucesso
      400:
        description: Campo 'turbidez' é obrigatório
    """
    
    data = request.get_json()

    if 'turbidez' not in data:
        return jsonify({"erro": "Campo 'turbidez' é obrigatório"}), 400

    nova_leitura = Turbidez(valor=data['turbidez'])
    db.session.add(nova_leitura)
    db.session.commit()

    return jsonify({"mensagem": "Leitura salva com sucesso!"}), 201
