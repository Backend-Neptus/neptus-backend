def register_client_routes(app):
    from app.controllers.v1 import (
    auth_controller,
    propriedade_controller
    )
    # ROTAS NÃO ADMINISTRATIVAS
    # Auth
    app.add_url_rule('/auth/register', 'register', auth_controller.register, methods=['POST'])
    app.add_url_rule('/auth/login', 'login', auth_controller.login, methods=['POST'])
    app.add_url_rule('/auth/refresh', 'refresh_token', auth_controller.refresh_token, methods=['POST'])
    app.add_url_rule('/auth/forgot-password', 'reset_password_request', auth_controller.reset_password_request, methods=['POST'])
    app.add_url_rule('/auth/reset-password', 'reset_password', auth_controller.reset_password, methods=['POST'])
    app.add_url_rule('/auth/login/google', 'authorize_google', auth_controller.authorize_google, methods=['POST'])

    app.add_url_rule('/v1/propriedades/usuarios/convites', 'convidar_usuario', propriedade_controller.convidar_usuario, methods=['POST'])
    app.add_url_rule('/v1/propriedades/usuarios/convites/aceite', 'convite_aceito', propriedade_controller.convite_aceito, methods=['POST'])


