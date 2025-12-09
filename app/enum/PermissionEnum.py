import enum


class PermissionEnum(enum.Enum):
    # Permissões para usuários
    USUARIO_LISTAR = "usuario_listar"
    USUARIO_DETALHAR = "usuario_detalhar"
    USUARIO_CRIAR = "usuario_criar"
    USUARIO_EDITAR = "usuario_editar"
    USUARIO_STATUS = "usuario_status"

    # Permissões para perfis
    PERFIL_LISTAR = "perfil_listar"
    PERFIL_DETALHAR = "perfil_detalhar"
    PERFIL_CRIAR = "perfil_criar"
    PERFIL_EDITAR = "perfil_editar"
    PERFIL_EXCLUIR = "perfil_excluir"

    # Permissões para propriedades
    PROPRIEDADE_LISTAR = "propriedade_listar"
    PROPRIEDADE_DETALHAR = "propriedade_detalhar"
    PROPRIEDADE_CRIAR = "propriedade_criar"
    PROPRIEDADE_EDITAR = "propriedade_editar"
    PROPRIEDADE_EXCLUIR = "propriedade_excluir"


    # Permissões para tanques
    TANQUE_CRIAR = "tanque_criar"
    TANQUE_LISTAR = "tanque_listar"
    TANQUE_EDITAR = "tanque_editar"
    TANQUE_DETALHAR = "tanque_detalhar"
    TANQUE_EXCLUIR = "tanque_excluir"

    # Permissões para leituras
    LEITURA_LISTAR = "leitura_listar"
    LEITURA_DETALHAR = "leitura_detalhar"
    LEITURA_POR_TANQUE = "leitura_por_tanque"
    LEITURA_CRIAR = "leitura_criar"
    LEITURA_EXCLUIR = "leitura_excluir"