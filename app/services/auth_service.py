from itsdangerous import URLSafeTimedSerializer
from app import db
from app.exceptions import (BadRequestError, ConflictRequestError,
                            UserDisabledError, GoogleLoginRequestError,
                            NotFoundRequestError, InvalidCredentialsError)
from app.models.usuario_model import Usuario
from app.utils import default_perfil, reset_password, create_token


class AuthService:

  def registrar_usuario(self, nome: str, email: str, senha: str):

    if (not nome) or (not email) or (not senha):
      raise BadRequestError(
          "Os campos 'nome', 'email' e 'senha' devem ser preenchidos")

    if Usuario.query.filter_by(email=email).first():
      raise ConflictRequestError("E-mail ja cadastrado")

    perfil = default_perfil.get_default_perfil()
    usuario = Usuario(nome=nome, email=email, perfil_id=perfil.id)
    usuario.set_senha(senha)
    db.session.add(usuario)
    db.session.commit()

    return {
        'messagem': "Usuário cadastrado com sucesso",
        'access_token': create_token.create_token(id=usuario.id,
                                                  nome=usuario.nome),
        'refresh_token': create_token.refresh_token(id=usuario.id)
    }

  def login(self, email: str, senha: str):
    usuario = Usuario.query.filter_by(email=email).first()

    if not usuario:
      raise NotFoundRequestError("Usuário não cadastrado")

    if not usuario.is_active:
      raise UserDisabledError("Usuário desativado")
      
    if not usuario.google_login:
      raise GoogleLoginRequestError(
          "Faça login com seu e-mail e senha.")
      
    if usuario.google_login:
      raise GoogleLoginRequestError(
          "Usuário cadastrado via Google, use o login com Google")

    if not usuario.verificar_senha(senha):
      raise InvalidCredentialsError("Email ou senha inválidos")

    return {
        'access_token': create_token.create_token(id=usuario.id,
                                                  nome=usuario.nome),
        'refresh_token': create_token.refresh_token(id=usuario.id),
        'mensagem': "Login efetuado com sucesso",
        'usuario': {
            'id': usuario.id,
            'nome': usuario.nome,
            'email': usuario.email,
            'perfil': usuario.perfil.nome,
            'is_admin': usuario.is_admin,
            'permissoes': usuario.perfil.permissoes
        },
    }

  def authorize_google(self, nome: str, email: str):

    usuario = Usuario.query.filter_by(email=email).first()
    
    if usuario and not usuario.google_login:
            raise GoogleLoginRequestError("Faça login com seu e-mail e senha.")
  
    if not usuario:
      perfil = default_perfil.get_default_perfil()
      usuario = Usuario(nome=nome,
                        email=email,
                        perfil_id=perfil.id,
                        google_login=True)
      db.session.add(usuario)
      db.session.commit()

    if not usuario.is_active:
      raise UserDisabledError("Usuário desativado")

    return {
        'access_token': create_token.create_token(id=usuario.id,
                                                  nome=usuario.nome),
        'refresh_token': create_token.refresh_token(id=usuario.id),
        'mensagem': "Login efetuado com sucesso",
        'usuario': {
            'id': usuario.id,
            'nome': usuario.nome,
            'email': usuario.email,
            'perfil': usuario.perfil.nome,
            'is_admin': usuario.is_admin,
            'permissoes': usuario.perfil.permissoes
        },
    }

  def recuperar_senha(self, email: str):
    usuario = Usuario.query.filter_by(email=email).first()

    s = URLSafeTimedSerializer("secret_key")
    token_reset = s.dumps(email, salt="salt_key")

    if not usuario:
      raise NotFoundRequestError("E-mail não encontrado")

    if not usuario.is_active:
      raise UserDisabledError("Usuário desativado")

    if usuario.google_login:
      raise GoogleLoginRequestError("Usuário cadastrado via Google")

    reset_password.enviar_senha(email, token_reset, usuario.nome)
    return "Caso exista uma conta cadastrada com este e-mail, um link para redefinir a senha foi enviado."

  def refresh_token(self, user_id: str):
    usuario = Usuario.query.get(user_id)
    if not usuario:
      raise NotFoundRequestError("Usuário nao encontrado")
    if not usuario.is_active:
      raise UserDisabledError("Usuário desativado")
    refresh_token = create_token.create_token(usuario.id, usuario.nome)
    return refresh_token

  def resetar_senha(self, token_reset: str, senha: str):
    s = URLSafeTimedSerializer("secret_key")
    email = s.loads(token_reset, salt="salt_key", max_age=3600)
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
