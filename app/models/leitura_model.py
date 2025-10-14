
from app import db
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
import uuid

class Leitura(db.Model):
    __tablename__ = 'leitura'
    
    # Chave primária
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid)
    valor = db.Column(db.Float, nullable=False)  # Valor puro 
    usuario_id = db.Column(UUID(as_uuid=True), db.ForeignKey('usuarios.id'), nullable=False)
    propriedade_id = db.Column(UUID(as_uuid=True), db.ForeignKey('propriedades.id'), nullable=False)
    criado_em = db.Column(db.DateTime, default=db.func.now())  # Quando foi registrado no sistema
    atualizado_em = db.Column(db.DateTime,
                            default=datetime.utcnow,
                            onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Leitura {self.valor} (Propriedade: {self.propriedade_id})>'

    def to_dict(self):
        return {
            'id': str(self.id),
            'valor': self.valor,
            'usuario_id': str(self.usuario_id),
            'propriedade_id': str(self.propriedade_id),
            'criado_em': self.criado_em.isoformat()
          }  