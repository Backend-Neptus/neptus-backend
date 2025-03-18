from config.config import 
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://neptus:6NTm0CWr5zoy7gzJB4Xi0wyRIiBJ1sbrVO3OBhr173rTjundhPhe5fVGr671dhqb@pgadmin.cloudsyntax.com.br:54333/neptus-teste'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Turbidez(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    valor = db.Column(db.String, nullable=False)

class Sensor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String, nullable=False)


with app.app_context():
    db.create_all()

@app.route('/leitura/turbidez', methods=['POST'])
def salvar_turbidez():
    data = request.get_json()

    if 'turbidez' not in data:
        return jsonify({"erro": "Campo 'turbidez' é obrigatório"}), 400

    nova_leitura = Turbidez(valor=data['turbidez'])
    db.session.add(nova_leitura)
    db.session.commit()


    return jsonify({"mensagem": "Leitura salva com sucesso!"}), 201

@app.route('/sensor', methods=['POST'])
def salvar_sensor():
    data = request.get_json()

    novo_sensor = Sensor()
    novo_sensor.nome = data['nome']
    db.session.add(novo_sensor)
    db.session.commit()
    return jsonify({"mensagem": "Leitura salva com sucesso!"}), 201

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
