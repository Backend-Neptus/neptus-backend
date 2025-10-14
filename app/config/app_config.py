import os

class APP_CONFIG:
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL',
        'postgresql://neptus:6NTm0CWr5zoy7gzJB4Xi0wyRIiBJ1sbrVO3OBhr173rTjundhPhe5fVGr671dhqb@pgadmin.cloudsyntax.com.br:54333/neptus-db'  # valor padrão (opcional)
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SECRET_KEY = os.getenv('SECRET_KEY', 'default-secret-key')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'default-jwt-secret-key')

    MAIL_SERVER = os.getenv('MAIL_SERVER', 'smtp.exemplo.com')
    MAIL_PORT = int(os.getenv('MAIL_PORT', 587))
    MAIL_USE_TLS = os.getenv('MAIL_USE_TLS', 'True') == 'True'
    MAIL_USERNAME = os.getenv('MAIL_USERNAME', 'email@exemplo.com')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD', 'senhaemail')
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER', 'email@exemplo.com')

    CONVITE_TOKEN_SECRET = os.getenv('CONVITE_TOKEN_SECRET', 'convite-secret')
    CONVITE_TOKEN_SALT = os.getenv('CONVITE_TOKEN_SALT', 'convite-salt')

    RESET_PASSWORD_TOKEN_SECRET = os.getenv('RESET_PASSWORD_TOKEN_SECRET', 'reset-secret')
    RESET_PASSWORD_TOKEN_SALT = os.getenv('RESET_PASSWORD_TOKEN_SALT', 'reset-salt')

    NEPTUS_URL = os.getenv('NEPTUS_URL', 'http://localhost:3000')

