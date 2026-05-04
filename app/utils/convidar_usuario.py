import random
import string
from flask_mail import Message
from app import mail
from app.config.app_config import APP_CONFIG

def enviar_convite(email_destino, token_convite, nome_propriedade=None, usuario_request=None, nome=None):
    msg = Message(
        subject='Neptus • Convite de acesso',
        sender=("Neptus - Suporte", "neptus@cloudsyntax.com.br"),
        recipients=[email_destino]
    )

    msg.html = f"""
        <html>
        <body style="font-family: Arial, sans-serif; background-color: #f0f2f5; padding: 20px;">
            <div style="max-width: 600px; margin: auto; background-color: #ffffff; padding: 30px; border-radius: 8px; box-shadow: 0px 0px 10px rgba(0,0,0,0.1);">
            <h2 style="color: #0d6efd; text-align: center;">Neptus</h2>
            <p style="font-size: 16px; color: #333;">Olá, {nome}.</p>
            <p style="font-size: 16px; color: #333;">
                Você foi convidado por {usuario_request} para se cadastrar e acessar a propriedade <strong>{nome_propriedade}</strong> no sistema <strong>Neptus</strong>.
            </p>
            <div style="background-color: #f8f9fa; padding: 15px; margin: 20px 0; border-radius: 5px; text-align: center; font-size: 20px; font-weight: bold; color: #212529;">
                <a href="{APP_CONFIG.NEPTUS_URL}/propriedade/convite/{token_convite}" style="color: #0d6efd; text-decoration: none; word-break: break-all;">Aceitar Convite</a>
            </div>
            <p style="font-size: 14px; color: #555;">
                Caso não consiga acessar o link acima, copie e cole o link abaixo no seu navegador:
                <br>
                <a href="{APP_CONFIG.NEPTUS_URL}/{token_convite}" style="color: #0d6efd; text-decoration: none; word-break: break-all;">{APP_CONFIG.NEPTUS_URL}/propriedade/convite/{token_convite}</a>
            </p>
            <hr style="margin-top: 30px;">
            <p style="font-size: 12px; color: #aaa; text-align: center;">
                <strong>Neptus</strong><br>
                Caso você tenha recebido este e-mail por engano, por favor, ignore-o.<br>
                Este e-mail foi enviado automaticamente pela plataforma <strong>Neptus</strong>. Por favor, não responda.
            </p>
            </div>
        </body>
        </html>
    """
    mail.send(msg)


  
  