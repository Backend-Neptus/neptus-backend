def register_client_routes(app):
    from app.controllers.v1 import (
    auth_controller,
    propriedade_controller,
    leitura_controller
    )
    # ROTAS NÃO ADMINISTRATIVAS
    # Auth
    app.add_url_rule('/auth/register', 'register', auth_controller.register, methods=['POST'])
    app.add_url_rule('/auth/login', 'login', auth_controller.login, methods=['POST'])
    app.add_url_rule('/auth/refresh', 'refresh_token', auth_controller.refresh_token, methods=['POST'])
    app.add_url_rule('/auth/forgot-password', 'reset_password_request', auth_controller.reset_password_request, methods=['POST'])
    app.add_url_rule('/auth/reset-password', 'reset_password', auth_controller.reset_password, methods=['POST'])
    app.add_url_rule('/auth/login/google', 'authorize_google', auth_controller.authorize_google, methods=['POST'])

    app.add_url_rule('/v1/propriedades/associadas', 'listar_leituras_usuarios', propriedade_controller.listar_leituras_usuarios, methods=['GET'])
    app.add_url_rule('/v1/propriedades/usuarios/convites', 'convidar_usuario', propriedade_controller.convidar_usuario, methods=['POST'])
    app.add_url_rule('/v1/propriedades/usuarios/convites/aceite', 'convite_aceito', propriedade_controller.convite_aceito, methods=['POST'])

    app.add_url_rule('/v1/leituras/', 'listar_leituras', leitura_controller.listar_leituras, methods=['GET'])
    app.add_url_rule('/v1/leituras/<leitura_id>', 'buscar_leitura', leitura_controller.buscar_leitura,methods=['GET'])
    app.add_url_rule('/v1/leituras', 'criar_leitura', leitura_controller.criar_leitura, methods=['POST'])
    app.add_url_rule('/v1/leituras/lote', 'criar_leituras_em_lote', leitura_controller.criar_leituras_em_lote, methods=['POST'])
    app.add_url_rule('/v1/leituras/<leitura_id>', 'atualizar_leitura',leitura_controller.atualizar_leitura, methods=['PUT'])
    app.add_url_rule('/v1/leituras/<leitura_id>', 'deletar_leitura', leitura_controller.deletar_leitura, methods=['DELETE'])
