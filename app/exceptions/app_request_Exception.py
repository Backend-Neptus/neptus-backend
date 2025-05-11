from werkzeug.exceptions import MethodNotAllowed
from flask import jsonify
from itsdangerous import BadTimeSignature, SignatureExpired
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

@app.errorhandler(SignatureExpired)
def handle_signature_exception(e):

    app_error = AppRequestError(
        message="Sessão expirada, por favor faça login novamente.",
        code=type(e).__name__, 
        status=401
    )
    return jsonify(app_error.to_dict()), 401

@app.errorhandler(BadTimeSignature)
def handle_bad_signature(e):
    app_error = AppRequestError(
        message="Token inválido ou corrompido.",
        code=type(e).__name__,
        status=400
    )
    return jsonify(app_error.to_dict()), 400

@app.errorhandler(MethodNotAllowed)
def handle_method_not_allowed(e):
    app_error = AppRequestError(
        message="Método HTTP não permitido para esta rota.",
        code=type(e).__name__,
        status=405
    )
    return jsonify(app_error.to_dict()), 405

@app.errorhandler(TimeoutError)
def handle_method_not_allowed(e):
    app_error = AppRequestError(
        message="O servidor demorou para responder. Tente novamente mais tarde.",
        code=type(e).__name__,
        status=408 
    )
    return jsonify(app_error.to_dict()), 408 
