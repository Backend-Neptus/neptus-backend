from datetime import datetime
import uuid
from sqlalchemy.dialects.postgresql import UUID
from app import db

class Leitura(db.Model):
    __tablename__ = 'leitura'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)
    valor = db.Column(db.Float, nullable=False)
    cor_agua = db.Column(db.Integer, nullable=False)
    oxigenio = db.Column(db.Float, nullable=False)   
    temperatura = db.Column(db.Float, nullable=False)  
    ph_agua = db.Column(db.Float, nullable=False)      
    amonia = db.Column(db.Float, nullable=False)       
    id_usuario = db.Column(UUID(as_uuid=True), db.ForeignKey('usuario.id'), nullable=True)
    id_tanque = db.Column(UUID(as_uuid=True), db.ForeignKey('tanque.id'), nullable=True)
    id_propriedade = db.Column(UUID(as_uuid=True), db.ForeignKey('propriedade.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relacionamentos
    usuario = db.relationship('Usuario', backref=db.backref('leituras', lazy=True))
    tanque = db.relationship('Tanque', backref=db.backref('leituras', lazy=True))
    propriedade = db.relationship('Propriedade', backref=db.backref('leituras', lazy=True))

    def to_dict(self):
        return {
            'id': self.id,
            'criado_em': self.criado_em.strftime('%d/%m/%Y %H:%M:%S'),
            'valor': self.valor,
            'cor_agua': self.cor_agua,
            'oxigenio': self.oxigenio,
            'temperatura': self.temperatura,
            'ph_agua': self.ph_agua,
            'amonia': self.amonia,
            'id_usuario': self.id_usuario,
            'id_tanque': self.id_tanque,
            'id_propriedade': self.id_propriedade,
            'usuario_nome': self.usuario.nome,
            'tanque_nome': self.tanque.nome,
            'propriedade_nome': self.propriedade.nome
        }