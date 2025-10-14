
from app import db
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
import uuid

class Leitura(db.Model):
    __tablename__ = 'leitura'
    
    # Chave primária
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    usuario_id = db.Column(UUID(as_uuid=True), db.ForeignKey('usuario.id'), nullable=False)
    tanque = db.Column(UUID(as_uuid=True), db.ForeignKey('tanque.id'), nullable=False)
    turbidez = db.Column(db.Float, nullable=False)  
    oxigenio = db.Column(db.Float, nullable=False)  
    temperatura = db.Column(db.Float, nullable=False)  
    ph = db.Column(db.Float, nullable=False)   
    amonia = db.Column(db.Float, nullable=False)   
    imagem_cor = db.Column(db.String(50), unique=False, nullable=False)
    criado_em = db.Column(db.DateTime, default=db.func.now())  # Quando foi registrado no sistema
    atualizado_em = db.Column(db.DateTime,
                            default=datetime.utcnow,
                            onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': str(self.id),
            'usuario_id': str(self.usuario_id),
            'tanque': str(self.tanque),
            'turbidez': self.turbidez,
            'oxigenio': self.oxigenio,
            'temperatura': self.temperatura,
            'ph': self.ph,
            'amonia': self.amonia,
            'imagem_cor': self.imagem_cor,
            'criado_em': self.criado_em.strftime('%d/%m/%Y %H:%M:%S'),
            'atualizado_em': self.atualizado_em.strftime('%d/%m/%Y %H:%M:%S'),
          }  