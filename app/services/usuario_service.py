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
from app.enum.PermissionEnum import PermissionEnum
from app.exceptions import (BadRequestError, ConflictRequestError,
                            UserDisabledError, GoogleLoginRequestError,
                            NotFoundRequestError, InvalidCredentialsError)


class UsuarioService():

  def registrar_usuario(nome: str, email: str, senha: str, perfil_id: str):

    if (not nome) or (not email) or (not senha) or (not perfil_id):
      raise BadRequestError(
          "Os campos 'nome', 'email', 'senha' e 'perfil_id' devem ser preenchidos"
      )

    if Usuario.query.filter_by(email=email).first():
      raise ConflictRequestError("E-mail ja cadastrado")

    perfil = Perfil.query.get(perfil_id)
    if not perfil:
      raise NotFoundRequestError("Perfil nao encontrado")

    usuario = Usuario(nome=nome, email=email, perfil_id=perfil.id)
    usuario.set_senha(senha)
    db.session.add(usuario)
    db.session.commit()

    return usuario

  def listar_usuarios(page: int, per_page: int):
    if per_page > 50:
      per_page = 50
    
    usuario = Usuario.query.paginate(page=page, per_page=per_page, error_out=False)
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
    resultado = db.session.execute(text(""" 
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
    <html>
    <head>
        <meta charset="utf-8">
        <style>
            body { font-family: Arial, sans-serif; }
            h1 { text-align: center; }
            table { width: 100%; border-collapse: collapse; margin-top: 20px; }
            th, td { border: 1px solid #ccc; padding: 8px; text-align: left; }
            th { background-color: #f2f2f2; }
            hr { margin: 40px 0; }
        </style>
    </head>
    <body>
        <h1>Relatório de Usuários</h1>
        {% for usuario in usuarios %}
            <h2>{{ usuario.nome }} ({{ usuario.email }})</h2>
            <p><strong>Google Login:</strong> {{ usuario.google_login }}</p>
            <p><strong>Admin:</strong> {{ 'Sim' if usuario.is_admin else 'Não' }} |
               <strong>Ativo:</strong> {{ 'Sim' if usuario.is_active else 'Não' }}</p>
            <p><strong>Perfil ID:</strong> {{ usuario.perfil_id }}</p>
            <p><strong>Criado em:</strong> {{ usuario.created_at }}</p>
            <p><strong>Atualizado em:</strong> {{ usuario.updated_at }}</p>
            <p><strong>Total de Propriedades:</strong> {{ usuario.total_propriedades }}</p>
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
            <hr>
        {% endfor %}
    </body>
    </html>
    """

    # Renderizar o template com os dados dos usuários
    template = Template(html_template)
    html_renderizado = template.render(usuarios=usuarios)

    # Configuração do wkhtmltopdf
    config = pdfkit.configuration(wkhtmltopdf='C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe')

    # Criar um arquivo temporário para armazenar o PDF
    with NamedTemporaryFile(delete=False, suffix=".pdf") as temp_pdf:
        temp_pdf_path = temp_pdf.name
        pdfkit.from_string(html_renderizado, temp_pdf_path, configuration=config)

    # Abrir o arquivo PDF gerado para leitura
    with open(temp_pdf_path, 'rb') as f:
        pdf_data = f.read()

    # Remover o arquivo temporário após leitura
    os.remove(temp_pdf_path)

    # Retornar o PDF gerado como resposta HTTP
    return Response(pdf_data, content_type='application/pdf',
                    headers={"Content-Disposition": "attachment; filename=relatorio_usuarios.pdf"})