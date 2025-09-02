import os

class APP_CONFIG:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'postgresql://neptus:6NTm0CWr5zoy7gzJB4Xi0wyRIiBJ1sbrVO3OBhr173rTjundhPhe5fVGr671dhqb@pgadmin.cloudsyntax.com.br:54333/tenant')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'neptus-chave-secreta'
    JWT_SECRET_KEY = 'jwt-chave-secreta'
    
    MAIL_SERVER = 'mail.cloudsyntax.com.br'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'neptus@cloudsyntax.com.br'
    MAIL_PASSWORD = 'y9UyPGZZ9tXahZdYuAZ4'
    MAIL_DEFAULT_SENDER = 'neptus@cloudsyntax.com.br'
    
    
    CONVITE_TOKEN_SECRET = 'convite-token-secret'
    CONVITE_TOKEN_SALT = 'convite-token-salt'
    
    RESET_PASSWORD_TOKEN_SECRET = 'reset-password-token-secret'
    RESET_PASSWORD_TOKEN_SALT = 'reset-password-token-salt'
    
    NEPTUS_URL = 'https://neptus.vercel.app'