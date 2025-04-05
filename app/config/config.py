import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'postgresql://neptus:6NTm0CWr5zoy7gzJB4Xi0wyRIiBJ1sbrVO3OBhr173rTjundhPhe5fVGr671dhqb@pgadmin.cloudsyntax.com.br:54333/neptus-teste')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'neptus-chave-secreta'
    JWT_SECRET_KEY = 'jwt-chave-secreta'