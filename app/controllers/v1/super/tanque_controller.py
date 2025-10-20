from flask import request, jsonify
from app.enum.PermissionEnum import PermissionEnum
from app.exceptions.app_request_Exception import AppRequestError
from app.services.tanque_service import TanqueService
from app.utils.permissoes import login_required, permission_required


@login_required
@permission_required(PermissionEnum.TANQUE_CRIAR)
def cadastrar_tanque():    
    data = request.get_json()
    try:
        nome = data.get('nome')
        id_propriedade = data.get('id_propriedade')
        area_tanque = data.get('area_tanque')
        tipo_peixe = data.get('tipo_peixe')
        peso_peixe = data.get('peso_peixe')
        qtd_peixe = data.get('qtd_peixe')

        tanque = TanqueService().cadastrar_tanque(
            nome=nome,
            id_propriedade=id_propriedade,
            area_tanque=area_tanque,
            tipo_peixe=tipo_peixe,
            peso_peixe=peso_peixe,
            qtd_peixe=qtd_peixe
        )

        return jsonify(tanque.to_dict()), 201

    except AppRequestError as e:
        return jsonify(e.to_dict()), e.status_code


@login_required
@permission_required(PermissionEnum.TANQUE_LISTAR)
def listar_tanques():    
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    try:
        resultado = TanqueService().listar_tanques(page, per_page)
        return jsonify(resultado), 200
    except AppRequestError as e:
        return jsonify(e.to_dict()), e.status_code


@login_required
@permission_required(PermissionEnum.TANQUE_EDITAR)
def detalhar_tanque(id):    
    try:
        tanque = TanqueService().exibir_tanque(id)
        return jsonify(tanque), 200
    except AppRequestError as e:
        return jsonify(e.to_dict()), e.status_code


@login_required
@permission_required(PermissionEnum.TANQUE_EDITAR)
def atualizar_tanque(id):    
    data = request.get_json()
    try:
        tanque = TanqueService().atualizar_tanque(id, data)
        return jsonify(tanque.to_dict()), 200
    except AppRequestError as e:
        return jsonify(e.to_dict()), e.status_code


@login_required
@permission_required(PermissionEnum.TANQUE_EDITAR)
def desativar_tanque(id):   
    try:
        tanque = TanqueService().desativar_tanque(id)
        return jsonify({
            "mensagem": f"Tanque '{tanque['nome']}' desativado com sucesso.",
            "tanque": tanque
        }), 200
    except AppRequestError as e:
        return jsonify(e.to_dict()), e.status_code