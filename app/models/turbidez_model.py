from app import db

class Turbidez(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    valor = db.Column(db.String, nullable=False)

    def __repr__(self):
        return f"<Turbidez {self.id}, {self.valor}>"