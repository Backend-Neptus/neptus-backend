from app.exceptions.app_request_Exception import AppRequestError

class UnauthorizedRequestError(AppRequestError):
  status_code = 403
  def __init__(self, message="Permissão negada"):
    super().__init__(message, code="UnauthorizedRequestError", status=401)
