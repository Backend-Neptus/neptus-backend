import datetime
from io import BytesIO
import os
from tempfile import NamedTemporaryFile
from flask import Response
from jinja2 import Template
import pdfkit
from sqlalchemy import text
from app import db
from app.models.usuario_model import Usuario
from app.models.perfil_model import Perfil
from app.exceptions import (BadRequestError, ConflictRequestError,
                            NotFoundRequestError)
from app.utils import pdfkit_config
from app.utils import default_perfil


class UsuarioService():

  def registrar_usuario(nome: str, email: str, senha: str, perfil_id: str):

    if (not nome) or (not email) or (not senha):
      raise BadRequestError(
          "Os campos 'nome', 'email' e 'senha' devem ser preenchidos"
      )

    if Usuario.query.filter_by(email=email).first():
      raise ConflictRequestError("E-mail ja cadastrado")
    
    perfil = default_perfil.get_default_perfil()
    usuario = Usuario(nome=nome, email=email, perfil_id=perfil.id)
    usuario.set_senha(senha)
    db.session.add(usuario)
    db.session.commit()

    return usuario

  def listar_usuarios(page: int, per_page: int):
    if per_page > 50:
      per_page = 50

    usuario = Usuario.query.order_by(Usuario.created_at).paginate(page=page,
                                     per_page=per_page,
                                     error_out=False)
    return {
        'total': usuario.total,
        'pagina_atual': usuario.page,
        'itens_por_pagina': usuario.per_page,
        'total_paginas': usuario.pages,
        'usuarios': [usuario.to_dict() for usuario in usuario]
    }

  def atualizar_usuario(id: str, nome: str, email: str, perfil_id: str):
    if (not nome) or (not email) or (not perfil_id):
      raise BadRequestError(
          "Os campos 'nome', 'email' e 'perfil_id' devem ser preenchidos")
    usuario = Usuario.query.get(id)

    if not usuario:
      raise NotFoundRequestError("Usuário não encontrado")

    perfil = Perfil.query.get(perfil_id)
    if not perfil:
      raise NotFoundRequestError("Perfil nao encontrado")

    if usuario.email != email:
      usuario_email = Usuario.query.filter_by(email=email).first()
      if usuario_email and usuario_email.id != usuario.id:
        raise ConflictRequestError("E-mail ja cadastrado")

    usuario.nome = nome
    usuario.email = email
    usuario.perfil_id = perfil_id
    db.session.commit()

    return usuario

  def status_usuario(id: str, status: bool):
    usuario = Usuario.query.get(id)

    if not usuario:
      raise NotFoundRequestError("Usuário nao encontrado")

    if status:
      usuario.is_active = True
    else:
      usuario.is_active = False

    db.session.commit()
    return usuario

  def buscar_usuario(id):
    usuario = Usuario.query.get(id)
    if not usuario:
      raise NotFoundRequestError("Usuário nao encontrado")
    return usuario


  def relatorio_usuarios():
    resultado = db.session.execute(
        text(""" 
        SELECT 
            u.id,
            u.nome,
            u.email,
            u.google_login,
            u.is_admin,
            u.is_active,
            u.perfil_id,
            to_char(u.created_at, 'DD/MM/YYYY HH24:MI:SS') AS created_at,
            to_char(u.updated_at, 'DD/MM/YYYY HH24:MI:SS') AS updated_at,
            COUNT(p.id) AS total_propriedades,
            COALESCE(json_agg(
                json_build_object(
                    'id', p.id,
                    'nome', p.nome
                )
            ) FILTER (WHERE p.id IS NOT NULL), '[]') AS propridedade
        FROM usuario u
        LEFT JOIN propriedade_usuarios up ON up.usuario_id = u.id
        LEFT JOIN propriedade p ON p.id = up.propriedade_id
        GROUP BY u.id
        ORDER BY u.created_at;
    """))

    # Transformar resultado da consulta em lista de dicionários
    usuarios = [dict(row._mapping) for row in resultado.fetchall()]

    # Template HTML para o relatório
    html_template = """
    <!DOCTYPE html>
    <html lang="pt-BR">
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Relatório de Usuários - Neptus</title>
        <style type="text/css">
            /* Estilos base */
            body {
                font-family: 'Segoe UI', Roboto, Arial, sans-serif;
                line-height: 1.6;
                color: #333;
                background-color: #fff;
                margin: 0;
                padding: 0;
            }
            
            .container {
                max-width: 1200px;
                margin: 0 auto;
                padding: 20px;
            }
            
            /* Cabeçalho */
            .header {
                display: flex;
                align-items: center;
                justify-content: space-between;
                padding: 20px 0;
                border-bottom: 1px solid #e2e8f0;
                margin-bottom: 40px;
            }
            
            .logo {
                display: flex;
                align-items: center;
            }
            
            .logo-img {
                height: 50px;
            }
            
            .logo-text {
                font-size: 24px;
                font-weight: 700;
                color: #0068B7;
                margin-left: 10px;
            }
            
            .date-info {
                font-size: 14px;
                color: #555;
            }
            
            .report-title {
                font-size: 24px;
                font-weight: 600;
                color: #333;
                text-align: center;
                margin-bottom: 40px;
            }
            
            /* Cards de usuário */
            .user-card {
                background-color: white;
                border-radius: 8px;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
                padding: 30px;
                margin-bottom: 30px;
            }
            
            .user-header {
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 20px;
            }
            
            .user-name {
                font-size: 22px;
                font-weight: 600;
                color: #0068B7;
                margin: 0;
            }
            
            .user-email {
                color: #666;
                font-size: 16px;
                margin: 5px 0 0 0;
            }
            
            /* Grid de informações */
            .user-info {
                display: grid;
                grid-template-columns: repeat(2, 1fr);
                gap: 15px;
                margin-bottom: 20px;
            }
            
            .info-item {
                margin-bottom: 10px;
            }
            
            .info-label {
                font-weight: 600;
                display: block;
                margin-bottom: 5px;
                color: #555;
                font-size: 14px;
            }
            
            .info-value {
                font-size: 15px;
            }
            
            /* Badges de status */
            .badge {
                display: inline-block;
                padding: 4px 8px;
                border-radius: 4px;
                font-size: 12px;
                font-weight: 600;
                color: white;
            }
            
            .badge-success {
                background-color: #38b2ac;
            }
            
            .badge-danger {
                background-color: #e53e3e;
            }
            
            /* Contador de propriedades */
            .properties-count {
                font-size: 16px;
                font-weight: 600;
                margin-bottom: 15px;
                color: #0068B7;
            }
            
            /* Tabela de propriedades */
            table {
                width: 100%;
                border-collapse: collapse;
                margin-top: 15px;
            }
            
            thead {
                background-color: #0068B7;
                color: white;
            }
            
            th, td {
                padding: 12px 15px;
                text-align: left;
                border-bottom: 1px solid #e2e8f0;
            }
            
            tbody tr:nth-child(even) {
                background-color: #f5f7fa;
            }
            
            /* Rodapé */
            .footer {
                text-align: center;
                margin-top: 50px;
                color: #666;
                font-size: 14px;
                padding-top: 20px;
                border-top: 1px solid #e2e8f0;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <div class="logo">
                    <svg class="logo-img" width="50" height="50" viewBox="0 0 200 100" xmlns="http://www.w3.org/2000/svg">
                        <path d="M40,40 L70,20 L100,40 L70,60 L40,40 Z" fill="#0068B7" />
                        <path d="M70,60 L100,40 L130,60 L100,80 L70,60 Z" fill="#00A3E0" />
                        <path d="M100,40 L130,20 L160,40 L130,60 L100,40 Z" fill="#72C8EB" />
                    </svg>
                    <div class="logo-text">NEPTUS</div>
                </div>
                <div class="date-info">
                    Data: {{ data_hoje }}
                </div>
            </div>

            <h1 class="report-title">Relatório de Usuários</h1>

            {% for usuario in usuarios %}
            <div class="user-card">
                <div class="user-header">
                    <div>
                        <h2 class="user-name">{{ usuario.nome }}</h2>
                        <p class="user-email">{{ usuario.email }}</p>
                    </div>
                    <div>
                        <span class="badge {% if usuario.is_active %}badge-success{% else %}badge-danger{% endif %}">
                            {{ 'Ativo' if usuario.is_active else 'Inativo' }}
                        </span>
                        {% if usuario.is_admin %}
                        <span class="badge badge-success">Admin</span>
                        {% endif %}
                    </div>
                </div>

                <div class="user-info">
                    <div class="info-item">
                        <span class="info-label">Google Login</span>
                        <span class="info-value">{{ usuario.google_login }}</span>
                    </div>
                    <div class="info-item">
                        <span class="info-label">Perfil ID</span>
                        <span class="info-value">{{ usuario.perfil_id }}</span>
                    </div>
                    <div class="info-item">
                        <span class="info-label">Criado em</span>
                        <span class="info-value">{{ usuario.created_at }}</span>
                    </div>
                    <div class="info-item">
                        <span class="info-label">Atualizado em</span>
                        <span class="info-value">{{ usuario.updated_at }}</span>
                    </div>
                </div>

                <div class="properties-count">
                    <span>Total de Propriedades: {{ usuario.total_propriedades }}</span>
                </div>

                {% if usuario.propridedade and usuario.propridedade != '[]' %}
                <table>
                    <thead>
                        <tr>
                            <th>ID da Propriedade</th>
                            <th>Nome da Propriedade</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% for prop in usuario.propridedade %}
                        <tr>
                            <td>{{ prop.id }}</td>
                            <td>{{ prop.nome }}</td>
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>
                {% else %}
                <p>Nenhuma propriedade registrada.</p>
                {% endif %}
            </div>
            {% endfor %}

            <div class="footer">
                <p>&copy; {{ data_hoje.split('/')[2] }} Neptus. Todos os direitos reservados.</p>
            </div>
        </div>
    </body>
    </html>
    """

    template = Template(html_template)
    html_renderizado = template.render(usuarios=usuarios, data_hoje=datetime.datetime.now().strftime('%d/%m/%Y'))

    # Opções específicas para o pdfkit renderizar corretamente o CSS
    options = {
        'encoding': 'UTF-8',
        'page-size': 'A4',
        'margin-top': '0.75in',
        'margin-right': '0.75in',
        'margin-bottom': '0.75in',
        'margin-left': '0.75in',
        'enable-local-file-access': None,
        'disable-smart-shrinking': None,
        'no-outline': None,
        'print-media-type': None
    }

    config = pdfkit_config.get_pdfkit_config()

    with NamedTemporaryFile(delete=False, suffix=".pdf") as temp_pdf:
      temp_pdf_path = temp_pdf.name
      pdfkit.from_string(html_renderizado, temp_pdf_path, configuration=config, options=options)

    with open(temp_pdf_path, 'rb') as f:
      pdf_data = f.read()

    os.remove(temp_pdf_path)

    return Response(pdf_data,
                    content_type='application/pdf',
                    headers={
                        "Content-Disposition":
                        "attachment; filename=relatorio_usuarios.pdf"
                    })