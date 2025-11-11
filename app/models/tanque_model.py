import uuid
from datetime import datetime, timezone
from sqlalchemy import UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from app import db

class Tanque(db.Model):
    __tablename__ = 'tanque'
    __table_args__ = (
        UniqueConstraint('id_propriedade', 'nome', name='uq_tanque_nome_propriedade'),
    )
    
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    id_usuario = db.Column(UUID(as_uuid=True), db.ForeignKey('usuario.id'))
    id_propriedade = db.Column(UUID(as_uuid=True), db.ForeignKey('propriedade.id'))
    nome = db.Column(db.String(50), nullable=False)
    area_tanque = db.Column(db.Float, nullable=False)
    tipo_peixe = db.Column(db.String(50), nullable=False)
    peso_peixe = db.Column(db.Float, nullable=True)
    qtd_peixe = db.Column(db.Integer, nullable=True)
    ativo = db.Column(db.Boolean, nullable=False, default=True)
    criado_em = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    atualizado_em = db.Column(db.DateTime,
                              default=lambda: datetime.now(timezone.utc),
                              onupdate=lambda: datetime.now(timezone.utc))

    def to_dict(self):
        return {
            'id': str(self.id),
            'id_usuario': str(self.id_usuario) if self.id_usuario else None,
            'id_propriedade': str(self.id_propriedade) if self.id_propriedade else None,
            'nome': self.nome,
            'area_tanque': self.area_tanque,
            'tipo_peixe': self.tipo_peixe,
            'peso_peixe': self.peso_peixe,
            'qtd_peixe': self.qtd_peixe,
            'ativo': self.ativo,
            'criado_em': self.criado_em.isoformat() if self.criado_em else None,
            'atualizado_em': self.atualizado_em.isoformat() if self.atualizado_em else None
        }
