import random
import string
from flask_mail import Message
from app import mail

def enviar_senha(email_destino, token_reset, nome=None):
    msg = Message(
        subject='Neptus • Sua nova senha',
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
            Uma nova senha foi gerada para sua conta. Use a senha abaixo para acessar o sistema:
          </p>
          <div style="background-color: #f8f9fa; padding: 15px; margin: 20px 0; border-radius: 5px; text-align: center; font-size: 20px; font-weight: bold; color: #212529;">
            <a href="http://localhost:5000/reset-password/{token_reset}" style="color: #0d6efd; text-decoration: none;">Redefinir Senha</a>
          </div>
          <p style="font-size: 14px; color: #555;">
            <p>Caso não consiga acessar o link acima, copie e cole o link abaixo no seu navegador:</p>
            <a href="http://localhost:5000/reset-password/{token_reset}" style="color: #0d6efd; text-decoration: none; nowrap;">http://localhost:5000/reset-password/{token_reset}</a>
          </p>
          <hr style="margin-top: 30px;">
          <p style="font-size: 12px; color: #aaa; text-align: center;">
            <strong>Neptus</strong><br>
            <p>Caso vocé tenha recebido este e-mail por engano, por favor, ignore-o.</p>
            Este e-mail foi enviado automaticamente pela plataforma <strong>Neptus</strong>. Por favor, não responda.
          </p>
        </div>
      </body>
    </html>
    """
    mail.send(msg)
        
def gerar_nova_senha(tamanho=10):
  caracteres = string.ascii_letters + string.digits
  return ''.join(random.choices(caracteres, k=tamanho))

  
  