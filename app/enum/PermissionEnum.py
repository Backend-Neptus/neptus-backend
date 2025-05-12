import enum


class PermissionEnum(enum.Enum):
    # Permissões para usuários
    USUARIO_LISTAR = "usuario_listar"
    USUARIO_DETALHAR = "usuario_detalhar"
    USUARIO_CRIAR = "usuario_criar"
    USUARIO_EDITAR = "usuario_editar"
    USUARIO_EXCLUIR = "usuario_excluir"

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


    # Permissões para gerenciamento de permissões
    PERMISSAO_LISTAR = "permissao_listar"
    PERMISSAO_DETALHAR = "permissao_detalhar"
    PERMISSAO_CRIAR = "permissao_criar"
    PERMISSAO_EXCLUIR = "permissao_excluir"

    # Permissões para tanques
    TANQUE_LISTAR = "tanque_listar"
    TANQUE_DETALHAR = "tanque_detalhar"
    TANQUE_CRIAR = "tanque_criar"
    TANQUE_EDITAR = "tanque_editar"
    TANQUE_EXCLUIR = "tanque_excluir"

    # Permissões para sensores
    SENSOR_LISTAR = "sensor_listar"
    SENSOR_DETALHAR = "sensor_detalhar"
    SENSOR_CRIAR = "sensor_criar"
    SENSOR_EDITAR = "sensor_editar"
    SENSOR_EXCLUIR = "sensor_excluir"

    # Permissões para leituras
    LEITURA_LISTAR = "leitura_listar"
    LEITURA_DETALHAR = "leitura_detalhar"
    LEITURA_POR_TANQUE = "leitura_por_tanque"
    LEITURA_POR_SENSOR = "leitura_por_sensor"
    LEITURA_CRIAR = "leitura_criar"
    LEITURA_EXCLUIR = "leitura_excluir"
    
    
    
    
    # Permissões perfil local
    
    ATRIBUIR_PERFIL = "atribuir_perfil"