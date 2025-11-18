import uuid
import random
from datetime import datetime, timedelta
from app import app, db
from app.models.usuario_model import Usuario
from app.models.perfil_model import Perfil
from app.models.propriedade_model import Propriedade
from app.models.tanque_model import Tanque
from app.models.leitura_model import Leitura


# ---------------------------------------------------------------------
# PERFIS
# ---------------------------------------------------------------------
def criar_perfis():
    print("Criando perfis...")

    admin = Perfil(
        nome="Administrador",
        permissoes=[
            "gerenciar_usuarios",
            "gerenciar_propriedades",
            "visualizar_tanques",
            "visualizar_leituras"
        ]
    )

    funcionario = Perfil(
        nome="Funcionário",
        permissoes=["visualizar_tanques", "adicionar_leituras"]
    )

    cliente = Perfil(
        nome="Cliente",
        permissoes=["visualizar_suas_propriedades", "visualizar_tanques"]
    )

    db.session.add_all([admin, funcionario, cliente])
    db.session.commit()

    return admin, funcionario, cliente



# ---------------------------------------------------------------------
# USUÁRIOS (20)
# ---------------------------------------------------------------------
def criar_usuarios(admin, funcionario, cliente):
    print("Criando usuários...")

    nomes = [
    "Bruno Tavares", "Adriano Figueiredo", "Wagner Campos", "Leandro Brito",
    "Marcelo Teixeira", "Fábio Cardoso", "Gustavo Nery", "Ricardo Bessa",
    "Anderson Ramos", "Fellipe Duarte", "Sandro Pires", "Patrick Oliveira",
    "Márcio Paiva", "Renato Rezende", "Júlio Matos", "Vitor Carvalho",
    "Alan Ribeiro", "Paulo Fonseca", "Douglas Almeida", "Caio Lacerda"
]

    usuarios = []

    for i, nome in enumerate(nomes):
        email = nome.lower().replace(" ", ".") + "@example.com"

        # Distribuir perfis:
        if i == 0:
            perfil = admin
        elif i <= 6:
            perfil = funcionario
        else:
            perfil = cliente

        u = Usuario(nome=nome, email=email, perfil=perfil)
        u.set_senha("123456")

        usuarios.append(u)
        db.session.add(u)

    db.session.commit()
    return usuarios



# ---------------------------------------------------------------------
# PROPRIEDADES (10)
# ---------------------------------------------------------------------
def criar_propriedades(usuarios):
    print("Criando propriedades...")

    nomes =  [
    "Fazenda Ouro Verde",
    "Sítio São Bento",
    "Recanto Bela Vista",
    "Estância Sol Nascente",
    "Fazenda Água Limpa",
    "Sítio Ventos do Norte",
    "Chácara Santa Vitória",
    "Rancho Três Lagoas",
    "Fazenda Campo Belo",
    "Sítio Horizonte Azul"
]

    propriedades = []

    # escolher 10 proprietários clientes
    proprietarios = [u for u in usuarios if u.perfil.nome == "Cliente"][:10]

    funcionarios = [u for u in usuarios if u.perfil.nome == "Funcionário"]

    for nome, proprietario in zip(nomes, proprietarios):
        p = Propriedade(nome=nome, proprietario=proprietario)

        # proprietário + todos funcionários têm acesso
        p.usuarios.extend([proprietario] + funcionarios)

        propriedades.append(p)
        db.session.add(p)

    db.session.commit()
    return propriedades



# ---------------------------------------------------------------------
# TANQUES
# ---------------------------------------------------------------------
def criar_tanques(propriedades, usuarios):
    print("Criando tanques...")

    tanques = []
    tipos_peixe = ["Tambaqui", "Tilápia", "Pacu", "Pirarucu", "Carpa", "Dourado", "Traíra"]

    for p in propriedades:
        qtd = random.randint(5, 10)  # 3 a 6 tanques por propriedade

        for i in range(1, qtd + 1):
            t = Tanque(
                id_usuario=random.choice(usuarios).id,
                id_propriedade=p.id,
                nome=f"Tanque {i} - {p.nome}",
                area_tanque=round(random.uniform(150, 600), 2),
                tipo_peixe=random.choice(tipos_peixe),
                peso_peixe=round(random.uniform(0.3, 3.0), 2),
                qtd_peixe=random.randint(300, 2000),
                ativo=True
            )
            db.session.add(t)
            tanques.append(t)

    db.session.commit()
    return tanques



# ---------------------------------------------------------------------
# LEITURAS
# ---------------------------------------------------------------------
def criar_leituras(tanques, usuarios):
    print("Criando leituras...")

    funcionarios = [u for u in usuarios if u.perfil.nome == "Funcionário"]

    for tanque in tanques:
        for _ in range(15):  # 15 leituras por tanque
            leitura = Leitura(
                usuario_id=random.choice(funcionarios).id,
                tanque=tanque.id,
                turbidez=round(random.uniform(1.5, 14), 2),
                oxigenio=round(random.uniform(3.5, 10), 2),
                temperatura=round(random.uniform(23, 36), 2),
                ph=round(random.uniform(6.4, 9.0), 2),
                amonia=round(random.uniform(0.01, 1.2), 2),
                imagem_cor=random.choice(["verde", "amarela", "marrom", "turva", "clara"]),
                criado_em=datetime.utcnow() - timedelta(days=random.randint(1, 30))
            )

            db.session.add(leitura)

    db.session.commit()
    print("Leituras criadas.")



# ---------------------------------------------------------------------
# EXECUÇÃO PRINCIPAL
# ---------------------------------------------------------------------
def popular_banco():
    print("\n========== INICIANDO POPULAÇÃO DO BANCO ==========\n")

    admin, func, cliente = criar_perfis()
    usuarios = criar_usuarios(admin, func, cliente)
    propriedades = criar_propriedades(usuarios)
    tanques = criar_tanques(propriedades, usuarios)
    criar_leituras(tanques, usuarios)

    print("\n========== BANCO POPULADO COM SUCESSO! ==========\n")



if __name__ == "__main__":
    from app import app  # importa o app criado no seu app.py

    with app.app_context():
        popular_banco()