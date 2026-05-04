from app.exceptions.app_request_Exception import AppRequestError


class ConflictRequestError(AppRequestError):
  status_code = 409
  def __init__(self, message="Conflito na requisicao"):
    super().__init__(message, code="ConflictRequestError", status=409)