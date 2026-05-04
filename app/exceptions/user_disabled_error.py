from app.exceptions.app_request_Exception import AppRequestError

class UserDisabledError(AppRequestError):
  status_code = 403
  def __init__(self, message="Usuario desabilitado"):
    super().__init__(message, code="UserDisabledError", status=403)
