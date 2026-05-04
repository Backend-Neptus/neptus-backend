from app.exceptions.app_request_Exception import AppRequestError


class BadRequestError(AppRequestError):
  status_code = 400
  def __init__(self, message="Requisicao invalida"):
    super().__init__(message, code="BadRequestError", status=400)
