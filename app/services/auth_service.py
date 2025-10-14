from itsdangerous import URLSafeTimedSerializer
from app import db
from app.config.app_config import APP_CONFIG
from app.exceptions import (UserDisabledError, GoogleLoginRequestError,
                            NotFoundRequestError, InvalidCredentialsError)
from app.models.usuario_model import Usuario
from app.utils import reset_password, create_token


class AuthService:

  # def registrar_usuario(self, nome: str, email: str, senha: str):

  #   if (not nome) or (not email) or (not senha):
  #     raise BadRequestError(
  #         "Os campos 'nome', 'email' e 'senha' devem ser preenchidos")

  #   if Usuario.query.filter_by(email=email).first():
  #     raise ConflictRequestError("E-mail ja cadastrado")

  #   perfil = default_perfil.get_default_perfil()
  #   usuario = Usuario(nome=nome, email=email, perfil_id=perfil.id)
  #   usuario.set_senha(senha)
  #   db.session.add(usuario)
  #   db.session.commit()

  #   return {
  #       'access_token': create_token.create_token(id=usuario.id,
  #                                                 nome=usuario.nome),
  #       'refresh_token': create_token.refresh_token(id=usuario.id),
  #       'mensagem': "Login efetuado com sucesso",
  #       'usuario': {
  #           'id': usuario.id,
  #           'nome': usuario.nome,
  #           'email': usuario.email,
  #           'perfil': usuario.perfil.nome,
  #           'is_admin': usuario.is_admin,
  #           'permissoes': usuario.perfil.permissoes
  #       },
  #   }

  def login(self, email: str, senha: str):
    usuario = Usuario.query.filter_by(email=email).first()

    if not usuario:
      raise NotFoundRequestError("Usuário não cadastrado")

    if not usuario.esta_ativo:
      raise UserDisabledError("Usuário desativado")
    

    if not usuario.verificar_senha(senha):
      raise InvalidCredentialsError("Email ou senha inválidos")

    return {
        'access_token': create_token.create_token(id=usuario.id,
                                                  nome=usuario.nome, email=usuario.email, isAdmin=usuario.e_admin, permissoes=usuario.perfil.permissoes, perfil=usuario.perfil.nome),
        'refresh_token': create_token.refresh_token(id=usuario.id)
    }

  # def authorize_google(self, nome: str, email: str):

  #   usuario = Usuario.query.filter_by(email=email).first()
  
  #   if not usuario:
  #     perfil = default_perfil.get_default_perfil()
  #     usuario = Usuario(nome=nome,
  #                       email=email,
  #                       perfil_id=perfil.id,
  #                       google_login=True)
  #     db.session.add(usuario)
  #     db.session.commit()

  #   if not usuario.google_login:
  #       raise GoogleLoginRequestError("Faça login com seu e-mail e senha.")

  #   if not usuario.is_active:
  #     raise UserDisabledError("Usuário desativado")

  #   return {
  #       'access_token': create_token.create_token(id=usuario.id,
  #                                                 nome=usuario.nome),
  #       'refresh_token': create_token.refresh_token(id=usuario.id),
  #       'mensagem': "Login efetuado com sucesso",
  #       'usuario': {
  #           'id': usuario.id,
  #           'nome': usuario.nome,
  #           'email': usuario.email,
  #           'perfil': usuario.perfil.nome,
  #           'is_admin': usuario.is_admin,
  #           'permissoes': usuario.perfil.permissoes
  #       },
  #   }

  def recuperar_senha(self, email: str):
    usuario = Usuario.query.filter_by(email=email).first()

    s = URLSafeTimedSerializer(APP_CONFIG.RESET_PASSWORD_TOKEN_SECRET)
    token_reset = s.dumps(email, salt=APP_CONFIG.RESET_PASSWORD_TOKEN_SALT)

    if not usuario:
      return "Enviamos um link para redefinir a senha."

    if not usuario.esta_ativo:
      return "Enviamos um link para redefinir a senha."

    reset_password.enviar_senha(email, token_reset, usuario.nome)
    return "Enviamos um link para redefinir a senha."

  def refresh_token(self, user_id: str):
    usuario = Usuario.query.get(user_id)
    if not usuario:
      raise NotFoundRequestError("Usuário nao encontrado")
    if not usuario.is_active:
      raise UserDisabledError("Usuário desativado")
    refresh_token = create_token.create_token(usuario.id, usuario.nome, usuario.e_admin, usuario.perfil.nome, usuario.perfil.permissoes, usuario.email)
    return refresh_token

  def resetar_senha(self, token_reset: str, senha: str):
    s = URLSafeTimedSerializer(APP_CONFIG.RESET_PASSWORD_TOKEN_SECRET)
    email = s.loads(token_reset, salt=APP_CONFIG.RESET_PASSWORD_TOKEN_SALT, max_age=3600)
    usuario = Usuario.query.filter_by(email=email).first()
    if not usuario:
      raise NotFoundRequestError("E-mail nao encontrado")
    if not usuario.is_active:
      raise UserDisabledError("Usuário desativado")
    if usuario.google_login:
      raise GoogleLoginRequestError("Usuário cadastrado via Google")
    usuario.set_senha(senha)
    db.session.commit()
    return "Senha redefinida com sucesso!"
