from datetime import datetime
import uuid
from sqlalchemy.dialects.postgresql import UUID
from app import db
from app.exceptions.not_found_request_error import NotFoundRequestError
from app.models.perfil_model import Perfil
from sqlalchemy import select, join
from app.models.utils.associacoes import propriedade_usuarios, propriedade_perfil

class Propriedade(db.Model):
  __tablename__ = 'propriedade'
  id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
  nome = db.Column(db.String(50), unique=True, nullable=False)
  usuarios = db.relationship('Usuario',
                             secondary=propriedade_usuarios,
                             back_populates='propriedades',
                             overlaps="propriedades,perfis")
  proprietario_id = db.Column(UUID(as_uuid=True), db.ForeignKey('usuario.id'))
  proprietario = db.relationship('Usuario', foreign_keys=[proprietario_id])
  created_at = db.Column(db.DateTime, default=datetime.utcnow)
  updated_at = db.Column(db.DateTime,
                         default=datetime.utcnow,
                         onupdate=datetime.utcnow)
  perfis = db.relationship('Perfil',
                           secondary=propriedade_perfil,
                           back_populates='propriedades',
                           overlaps="usuarios")

  def to_dict(self):
    return {
        'id': self.id,
        'nome': self.nome,
        'total_usuarios': len(self.usuarios),
        'usuarios': [usuario.usuarios_to_dict() for usuario in self.usuarios],
        'proprietario_id': self.proprietario_id,
        'proprietario_nome': self.proprietario.nome,
        'perfis': [perfil.to_dict() for perfil in self.perfis],
        'created_at': self.created_at.strftime('%d/%m/%Y %H:%M:%S'),
        'updated_at': self.updated_at.strftime('%d/%m/%Y %H:%M:%S')
    }

  @staticmethod
  def __get_perfil_local(usuario_id, propriedade_id):
    stmt = select(propriedade_usuarios.c.perfil_local).where(
        propriedade_usuarios.c.usuario_id == usuario_id,
        propriedade_usuarios.c.propriedade_id == propriedade_id)
    result = db.session.execute(stmt).scalar()
    return result

  def get_perfil_local_do_usuario(self, usuario_id):
    perfil_id = self.__get_perfil_local(usuario_id, self.id)
    if perfil_id:
      return Perfil.query.get(perfil_id)
    raise NotFoundRequestError("Perfil local não encontrado")

  def listar_perfis_locais(propriedade_id):
    j = join(propriedade_usuarios, Perfil,
             propriedade_usuarios.c.perfil_local == Perfil.id)

    stmt = select(Perfil).select_from(j).where(
        propriedade_usuarios.c.propriedade_id == propriedade_id).distinct()

    resultados = db.session.execute(stmt).scalars().all()
    return [perfil.to_dict() for perfil in resultados]
