from flask import jsonify
from app import app

class AppRequestError(Exception):
    def __init__(self, message, code="AppRequestError", status=400):
        super().__init__(message)
        self.message = message
        self.code = code
        self.status = status

    def to_dict(self):
        return {
            "code": self.code,
            "message": self.message,
            "status": self.status
        }
        
@app.errorhandler(AppRequestError)
def handle_app_request_error(e):
    return jsonify(e.to_dict()), e.status


@app.errorhandler(Exception)
def handle_unexpected_exception(e):

    app_error = AppRequestError(
        message=str(e),
        code=type(e).__name__, 
        status=500
    )
    return jsonify(app_error.to_dict()), 500

@app.errorhandler(Exception)
def handle_signature_exception(e):

    app_error = AppRequestError(
        message="Sessão expirada, por favor faça login novamente.",
        code=type(e).__name__, 
        status=401
    )
    return jsonify(app_error.to_dict()), 401