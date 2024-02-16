from .database import db
from datetime import datetime, timedelta

class Client(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  nom = db.Column(db.String(80), nullable=False)
  email = db.Column(db.String(80), nullable=False, unique=True)
  reservations = db.relationship('Reservation', backref='client', lazy=True)

class Chambre(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  numero = db.Column(db.Integer, nullable=False, unique=True)
  type = db.Column(db.String(80))
  prix = db.Column(db.Float)
  reservations = db.relationship('Reservation', backref='chambre', lazy=True)

class Reservation(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  id_client = db.Column(db.Integer, db.ForeignKey('client.id'), nullable=False)
  id_chambre = db.Column(db.Integer, db.ForeignKey('chambre.id'), nullable=False)
  date_arrivee = db.Column(db.DateTime, nullable=False, default=datetime.now)
  date_depart = db.Column(db.DateTime, nullable=True, default = datetime.now()+timedelta(days=1))
  statut = db.Column(db.String(80), nullable=False)


