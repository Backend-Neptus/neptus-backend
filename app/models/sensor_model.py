from app import db


class Sensor(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  nome = db.Column(db.String, nullable=False)

  def __repr__(self):
    return f"<Sensor {self.id}, {self.nome}>"
