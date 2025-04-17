import datetime
import uuid
from flask import request, jsonify
from app import db
from app.exceptions import BadRequestError, ConflictRequestError, NotFoundRequestError
from app.models.usuario_model import Usuario
from app.models.perfil_model import Perfil
from app.utils.permissoes import permission_required, login_required
from app.enum.PermissionEnum import PermissionEnum
from app.services.usuario_service import UsuarioService
import pdfkit
from flask import  render_template_string, make_response

@login_required
@permission_required(PermissionEnum.USUARIO_CRIAR)
def salvar_usuario():
  """
    Cadastra um novo usuário.
    ---
    tags:
      - Usuários
    consumes:
      - application/json
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            id:
              type: string  # Mudado de integer para string (UUID)
              example: "51b03e1a-f849-438e-951a-f19a27b35902" 
            nome:
              type: string
              example: "Guido van Rossum"
            email:
              type: string
              example: "email@example.com"
            senha:
              type: string
              example: "123456"
            perfil_id:
              type: string 
              example: "1a7e8be3-b9b1-43a0-a04d-47dfb91372db" 
    responses:
      201:
        description: Usuário cadastrado com sucesso!
      400:
        description: Campos obrigatórios ausentes ou e-mail já cadastrado
"""
  data = request.get_json()

  try:
    nome = data.get('nome')
    email = data.get('email')
    senha = data.get('senha')
    perfil_id = data.get('perfil_id')
    return jsonify({
        'messagem':
        'Usuário cadastrado com sucesso',
        'data':
        UsuarioService.registrar_usuario(nome, email, senha,
                                         perfil_id).to_dict()
    }), 201
  except BadRequestError as e:
    return jsonify({"erro": e.message}), 400
  except ConflictRequestError as e:
    return jsonify({"erro": e.message}), 409
  except NotFoundRequestError as e:
    return jsonify({"erro": e.message}), 404


@login_required
@permission_required(PermissionEnum.USUARIO_LISTAR)
def listar_usuarios():
  """
    Lista todos os usuários cadastrados.
    ---
    tags:
      - Usuários
    responses:
      200:
        description: Lista de usuários
    """
  return jsonify(UsuarioService.listar_usuarios()), 200


@login_required
@permission_required(PermissionEnum.USUARIO_EDITAR)
def atualizar_usuario(id):
  """
    Atualiza os dados de um usuário existente.
    ---
    tags:
      - Usuários
    parameters:
      - in: path
        name: id
        required: true
        type: string  # Mudado de integer para string (UUID)
        example: "51b03e1a-f849-438e-951a-f19a27b35902"  
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            nome:
              type: string
              example: "Novo Nome"
            email:
              type: string
              example: "novo@email.com"
            senha:
              type: string
              example: "nova_senha"
            perfil_id:
              type: string  # Mudado de integer para string (UUID)
              example: "1a7e8be3-b9b1-43a0-a04d-47dfb91372db"  
    responses:
      200:
        description: Usuário atualizado com sucesso!
      404:
        description: Usuário não encontrado
"""

  data = request.get_json()

  try:
    return jsonify({
        "mensagem":
        "Usuário atualizado com sucesso!",
        "data":
        UsuarioService.atualizar_usuario(id, data['nome'], data['email'],
                                         data['perfil_id']).to_dict()
    }), 200
  except BadRequestError as e:
    return jsonify({"erro": e.message}), 400
  except ConflictRequestError as e:
    return jsonify({"erro": e.message}), 409
  except NotFoundRequestError as e:
    return jsonify({"erro": e.message}), 404


@login_required
@permission_required(PermissionEnum.USUARIO_EDITAR)
def status_usuario(id):
  """
    Ativar/Desativa um usuário existente.
    ---
    tags:
      - Usuários
    parameters:
      - in: path
        name: id
        required: true
        type: string  # Mudado de integer para string (UUID)
        example: "51b03e1a-f849-438e-951a-f19a27b35902"  
    responses:
      200:
        description: Usuário ativado/desativado com sucesso!
      404:
        description: Usuário nao encontrado
  """
  data = request.get_json()
  try:
    usuario = UsuarioService.status_usuario(id, data['status'])
    return jsonify({
        "mensagem":
        f"Usuário {'ativado' if usuario.is_active else 'desativado'} com sucesso!",
        "data": usuario.to_dict()
    }), 200

  except NotFoundRequestError as e:
    return jsonify({"erro": e.message}), 404


@login_required
@permission_required(PermissionEnum.USUARIO_DETALHAR)
def buscar_usuario(id):
  """
    Busca um usuário existente.
    ---
    tags:
      - Usuários
    parameters:
      - in: path
        name: id
        required: true
        type: string  # Mudado de integer para string (UUID)
        example: "51b03e1a-f849-438e-951a-f19a27b35902"  
    responses:
      200:
        description: Usuário encontrado com sucesso!
      404:
        description: Usuário nao encontrado
  """
  try:
    return jsonify(UsuarioService.buscar_usuario(id).to_dict()), 200
  except NotFoundRequestError as e:
    return jsonify({"erro": e.message}), 404


def relatorio_usuarios():
  usuarios = UsuarioService.listar_usuarios()
  template = """
      <!DOCTYPE html>
      <html lang="pt-br">

      <head>
          <meta charset="UTF-8">
          <title>Relatório - Neptus</title>
          <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.5/dist/css/bootstrap.min.css" rel="stylesheet"
              integrity="sha384-SgOJa3DmI69IUzQ2PVdRZhwQ+dy64/BUtbMJw1MZ8t5HZApcHrRKUc4W0kG879m7" crossorigin="anonymous">
          <style>
              body {
                  font-family: Arial, sans-serif;
                  margin: 40px;
                  color: #333;
              }

              .relatorio-header {
                  display: flex;
                  justify-content: space-between;
                  border-bottom: 2px solid #0077cc;
                  padding-bottom: 10px;
                  margin-bottom: 30px;
              }

              .logo h1 {
                  color: #0077cc;
                  margin: 0;
              }

              .empresa-info p {
                  margin: 2px 0;
              }

              .relatorio-conteudo {
                  min-height: 500px;
                  padding-bottom: 50px;
              }

              .relatorio-footer {
                  border-top: 1px solid #ccc;
                  font-size: 0.9em;
                  text-align: center;
                  color: #777;
                  padding-top: 15px;
                  margin-top: 30px;
              }
          </style>
      </head>

      <body>

          <!-- Cabeçalho -->
          <header class="relatorio-header">
              <div class="row">
                <div class="logo">
                    <h1>Neptus</h1> <!-- Pode substituir por uma imagem se quiser -->
                    <!-- <img src="{{ url_for('static', filename='imagens/logo.png') }}" alt="Logo Neptus"> -->
                </div>
                <div class="empresa-info">
                    <p><strong>Empresa:</strong> {{ empresa.nome }}</p>
                    <p><strong>Endereço:</strong> {{ empresa.endereco }}</p>
                    <p><strong>Telefone:</strong> {{ empresa.telefone }}</p>
                    <p><strong>Email:</strong> {{ empresa.email }}</p>
                </div>
              </div>
          </header>
          <!-- Conteúdo principal do relatório -->
          <main class="relatorio-conteudo">
              <div class="container-fluid">
                  <div class="row">
                      <div class="col-12">
                          <table class="table">
                              <thead>
                                  <tr>
                                      <th scope="col">Nome</th>
                                      <th scope="col">Email</th>
                                      <th scope="col">Status</th>
                                      <th scope="col">Perfil</th>
                                      <th scope="col">Propriedade</th>
                                      <th scope="col">Criado em</th>
                                  </tr>
                              </thead>
                              <tbody>
                                  {% for usuario in usuarios %}
                                  <tr>
                                      <td>{{ usuario.nome }}</td>
                                      <td>{{ usuario.email }}</td>
                                      <td>{{ 'Ativo' if usuario.is_active else 'Inativo' }}</td>
                                      <td>{{ usuario.perfil }}</td>
                                      <td>
                                        {% if usuario.propriedades %}
                                          <ul>
                                            {% for propriedade in usuario.propriedades %}
                                              <p>{{ propriedade.propriedade_nome }}</p>
                                            {% endfor %}
                                          </ul>
                                        {% else %}
                                          Sem propriedades
                                        {% endif %}
                                      </td>
                                      <td>{{ usuario.created_at }}</td>
                                  </tr>
                                  {% endfor %}
                              </tbody>
                          </table>
                      </div>
                  </div>
              </div>
          </main>

          <!-- Rodapé -->
          <footer class="relatorio-footer">
              <p>Relatório gerado por: <strong>{{ usuario.nome }}</strong> em <strong>{{ data_emissao }}</strong></p>
              <p>&copy; {{ ano_atual }} Neptus. Todos os direitos reservados.</p>
          </footer>

      </body>

      </html>
  """
  empresa = {
      "nome": "Neptus",
      "endereco": "Rua da Neptus, 123",
      "telefone": "1234567890",
      "email": "neptus@email"
      }
  usuario = {
      "nome": "Neptus",
      "email": "neptus@email"
  }
  data_emissao = "17/04/2025"
  ano_atual = "2025"
  rendered_html = render_template_string(template, usuarios=usuarios, data_emissao=data_emissao, ano_atual=ano_atual, empresa=empresa, usuario=usuario)
  
  wkhtmltopdf_path = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
  config = pdfkit.configuration(wkhtmltopdf=wkhtmltopdf_path)
  # Gerando o PDF com pdfkit
  pdf = pdfkit.from_string(rendered_html, False, configuration=config)
  uuid_str = str(uuid.uuid4())
  # Retornando o PDF como resposta
  response = make_response(pdf)
  response.headers["Content-Type"] = "application/pdf"
  response.headers["Content-Disposition"] = "attachment; filename=" + uuid_str + "_relatorio_usuarios.pdf"
    
  return response