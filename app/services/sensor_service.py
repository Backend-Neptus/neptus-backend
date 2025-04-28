from app import db
from app.models.sensor_model import Sensor
from app.models.usuario_model import Usuario
from app.models.tanque_model import Tanque
from app.models.propriedade_model import Propriedade
from app.exceptions import BadRequestError, NotFoundRequestError, ConflictRequestError
from flask import g

class SensorService:

    def criar_sensor(self, propriedade_id: str, nome: str, tanque_id: str):
        usuario_request = g.usuario
        if not usuario_request:
            raise NotFoundRequestError("Usuário não autenticado")

        propriedade = Propriedade.query.get(propriedade_id)
        if not propriedade:
            raise NotFoundRequestError("Propriedade não encontrada")

        if Sensor.query.filter_by(nome=nome, propriedade_id=propriedade_id).first():
            raise ConflictRequestError("Já existe um sensor com este nome nesta propriedade.")

        tanque = Tanque.query.get(tanque_id)
        if not tanque:
            raise NotFoundRequestError("Tanque não encontrado.")

        novo_sensor = Sensor(
            usuario_id=usuario_request.id,
            propriedade_id=propriedade_id,
            nome=nome,
            tanque=tanque
        )

        db.session.add(novo_sensor)
        db.session.commit()
        return novo_sensor

    def listar_sensores(self):
        sensores = db.session.query(Sensor).options(db.joinedload(Sensor.tanque)).all()
        return [sensor.to_dict() for sensor in sensores]

    def obter_sensor(self, sensor_id: str):
        sensor = db.session.query(Sensor).options(db.joinedload(Sensor.tanque)).get(sensor_id)
        if not sensor:
            raise NotFoundRequestError("Sensor não encontrado.")
        return sensor.to_dict()

    def atualizar_sensor(self, sensor_id: str, propriedade_id: str = None, nome: str = None, tanque_id: str = None):
        sensor = Sensor.query.get(sensor_id)
        if not sensor:
            raise NotFoundRequestError("Sensor não encontrado.")

        usuario_request = g.usuario
        if not usuario_request:
            raise NotFoundRequestError("Usuário não autenticado")

        if propriedade_id:
            propriedade = Propriedade.query.get(propriedade_id)
            if not propriedade:
                raise NotFoundRequestError("Propriedade não encontrada.")
            sensor.propriedade_id = propriedade_id

        if nome:
            if Sensor.query.filter_by(nome=nome, propriedade_id=sensor.propriedade_id).filter(Sensor.id != sensor_id).first():
                raise ConflictRequestError("Já existe sensor com este nome nesta propriedade.")
            sensor.nome = nome

        if tanque_id:
            tanque = Tanque.query.get(tanque_id)
            if not tanque:
                raise NotFoundRequestError("Tanque não encontrado.")
            sensor.tanque = tanque

        db.session.commit()
        return sensor

    def deletar_sensor(self, sensor_id: str):
        sensor = Sensor.query.get(sensor_id)
        if not sensor:
            raise NotFoundRequestError("Sensor não encontrado.")

        usuario_request = g.usuario
        if not usuario_request:
            raise NotFoundRequestError("Usuário não autenticado")

        db.session.delete(sensor)
        db.session.commit()