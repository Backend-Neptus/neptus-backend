def register_super_routes(app):
    from app.controllers.v1.super import (
    perfil_controller,
    propriedade_controller,
    usuario_controller,
    )
    # ROTAS ADMINISTRATIVAS

    # Perfis
    app.add_url_rule('/v1/super/perfis', 'salvar_perfil', perfil_controller.salvar_perfil, methods=['POST'])
    app.add_url_rule('/v1/super/perfis', 'listar_perfil', perfil_controller.listar_perfil, methods=['GET'])
    app.add_url_rule('/v1/super/perfis/<string:id>', 'atualizar_perfil', perfil_controller.atualizar_perfil, methods=['PUT'])
    app.add_url_rule('/v1/super/perfis/<string:id>', 'deletar_perfil', perfil_controller.deletar_perfil, methods=['DELETE'])
    app.add_url_rule('/v1/super/perfis/<string:id>', 'buscar_perfil', perfil_controller.buscar_perfil, methods=['GET'])

    # Usuários
    app.add_url_rule('/v1/super/usuarios', 'salvar_usuario', usuario_controller.salvar_usuario, methods=['POST'])
    app.add_url_rule('/v1/super/usuarios', 'listar_usuarios', usuario_controller.listar_usuarios, methods=['GET'])
    app.add_url_rule('/v1/super/usuarios/<string:id>', 'atualizar_usuario', usuario_controller.atualizar_usuario, methods=['PUT'])
    app.add_url_rule('/v1/super/usuarios/<string:id>', 'status_usuario', usuario_controller.status_usuario, methods=['PATCH'])
    app.add_url_rule('/v1/super/usuarios/<string:id>', 'buscar_usuario', usuario_controller.buscar_usuario, methods=['GET'])
    app.add_url_rule('/v1/super/usuarios/relatorio', 'relatorio_usuarios', usuario_controller.relatorio_usuarios, methods=['GET'])

    # Propriedades
    app.add_url_rule('/v1/super/propriedades', 'cadastrar_propriedade', propriedade_controller.cadastrar_propriedade, methods=['POST'])
    app.add_url_rule('/v1/super/propriedades', 'listar_propriedades', propriedade_controller.listar_propriedades, methods=['GET'])
    app.add_url_rule('/v1/super/propriedades/<string:id>', 'atualizar_propriedade', propriedade_controller.atualizar_propriedade, methods=['PUT'])
    app.add_url_rule('/v1/super/propriedades/<string:id>', 'detalhar_propriedade', propriedade_controller.detalhar_propriedade, methods=['GET'])
    app.add_url_rule('/v1/super/propriedades/usuarios/adicionar', 'adicionar_usuario', propriedade_controller.adicionar_usuario, methods=['POST'])
    app.add_url_rule('/v1/super/propriedades/usuarios/remover', 'remover_usuario', propriedade_controller.remover_usuario, methods=['POST'])
