
from app import db
from app.models.perfil_model import Perfil

def get_default_perfil():
    perfil = db.session.query(Perfil).filter(Perfil.nome == "Usuario").first()

    if not perfil:
        perfil = Perfil(
            nome="Usuario",
            permissoes=[
                # Permissões para tanques
                "tanque_listar",
                "tanque_detalhar",
                "tanque_criar",
                "tanque_editar",
                "tanque_excluir",
                # Permissões para sensores
                "sensor_listar",
                "sensor_detalhar",
                "sensor_criar",
                "sensor_editar",
                "sensor_excluir",
                # Permissões para leituras
                "leitura_listar",
                "leitura_detalhar",
                "leitura_por_tanque",
                "leitura_por_sensor",
                "leitura_criar",
                "leitura_excluir"
            ]
        )
        db.session.add(perfil)
        db.session.commit()

    return perfil