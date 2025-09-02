'''Contém a regra de negócio. O Controller chama o Service, que executa validações, interage com o banco de dados e aplica a lógica necessária.
Exemplo: Um método criarUsuario() que verifica se o e-mail já existe antes de salvar.

Cliente -> Controller -> Service -> Model -> Banco
'''

from app import db
from app.exceptions import BadRequestError, ConflictRequestError, NotFoundRequestError
from app.enum.PermissionEnum import PermissionEnum
from app.models.sensor_model import Sensor


class Sensorservice:

    #Get - chamar todos os sensores
    def listar_todos_sensores(id, page, per_page):
        if PermissaoPerfilLocal().verificar_permissao_perfil_local(permissao=PermissionEnum.SENSOR_LISTAR, id=id):
            if per_page > 50:
                per_page = 50
                sensores = Sensor.query.order_by(Sensor.created_at).paginate(
                page=page, per_page=per_page, error_out=False)
                return {
        'total': sensores.total,
        'pagina_atual': sensores.page,
        'itens_por_pagina': sensores.per_page,
        'total_paginas': sensores.pages,
        'sensores': [sensor.to_dict() for sensor in sensores]
    }
        else:
            raise NotFoundRequestError("Não foi possivel")

    #Get - chamar id de um sensor
    def chamar_id_sensor(id):
        sensor = Sensor.query.filter_by(id=id).first()  
        if sensor:
            if PermissaoPerfilLocal().verificar_permissao_perfil_local(permissao=PermissionEnum.SENSOR_DETALHAR, id= id):
                return sensor.to_dict()
        else:
            raise NotFoundRequestError("Sensor nao encontrado")

    #Post - criar novo sensor
    def criar_sensor(id, nome = str):
        if db.session.query(Sensor).filter_by(nome=nome).first() is not None:
            raise ConflictRequestError("Sensor com esse nome ja cadastrado")
        else:
            if PermissaoPerfilLocal().verificar_permissao_perfil_local(permissao=PermissionEnum.SENSOR_CRIAR, id=id):
                sensor = Sensor(nome=nome)
                db.session.add(sensor)
                db.session.commit()

    #Put - atualizar sensor
    def atualizar_sensor(id: str, nome: str, self):
        if not nome:
            raise BadRequestError("O campo 'nome' deve ser preenchido")
        sensor = self.sensor_existe(id)
        if PermissaoPerfilLocal().verificar_permissao_perfil_local(permissao=PermissionEnum.SENSOR_EDITAR, id=id):
            sensor.nome = nome.strip()  # Remove espaços extras
            sensor.save()

    # Delete - deletar sensor
    def deletar_sensor(self, id: str, nome : str = None):
        sensor = self.sensor_existe(id)
        if sensor is not None:
            if PermissaoPerfilLocal().verificar_permissao_perfil_local(permissao=PermissionEnum.SENSOR_EXCLUIR, id= id):
                db.session.delete(sensor)
                db.session.commit()
        else:
            raise ConflictRequestError("Não tem permissão para deletar")
     
    #Conferir se 
    
    #Conferir se o sensor existe
    def sensor_existe(id):
        sensor_id = Sensor.query.get(id)
        if not sensor_id:
            raise NotFoundRequestError("Sensor não encontrado")
        return sensor_id
