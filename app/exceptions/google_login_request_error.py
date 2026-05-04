
from app.exceptions.app_request_Exception import AppRequestError


class GoogleLoginRequestError(AppRequestError):
  status_code = 400
  def __init__(self, message="Requisicao invalida"):
    super().__init__(message, code="GoogleLoginRequestError", status=400)
