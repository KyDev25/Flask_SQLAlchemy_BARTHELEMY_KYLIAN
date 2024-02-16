from flask import Blueprint, request, jsonify
from ..models import Chambre, Reservation
from ..database import db
from datetime import datetime

reservation = Blueprint('reservation', __name__)

@reservation.route('/api/reservations', methods=['POST'])
def add_reservation():
  """
  Description: Ajouter une reservation.

  Vérifications:
  - Si la date d'arrivee est inferieure à la date de depart (#*1)
  - S'il n'y a des paramètres dans le body (#*2)
  - Si la date d'arrivee ou la date de depart est comprise dans l'intervalle (#*3)

  Etapes:
  - On parcours la liste de toutes les chambres (#*4)

  Résultat: Réservation créée avec succès.
  """
  data = request.get_json()
  getAllReservations = Reservation.query.join(Chambre).filter(Chambre.id == data['id_chambre']).all()
  arrival_date = datetime.strptime(data['date_arrivee'],'%Y-%m-%d')
  departure_date = datetime.strptime(data['date_depart'],'%Y-%m-%d')

  #*1
  if arrival_date > departure_date:
    return jsonify({'success': False, 'message': 'La date d\'arrivee doit être inferieure à la date de depart'})

  #*2
  if not data:
    return jsonify({'success': False, 'message': 'Réservation non créée'})

  #*4
  for reservation in getAllReservations:
    #*3
    if ((arrival_date <= reservation.date_depart <= departure_date) or (arrival_date <= reservation.date_arrivee <= departure_date)) or ((arrival_date == reservation.date_depart and departure_date == reservation.date_depart) or (arrival_date == reservation.date_arrivee and departure_date == reservation.date_arrivee)):
      return jsonify({'success': False, 'message': 'Cette Chambre est déjà réservée dans cet intervalle de temps.'})

  getReservation = Reservation(id_client=data['id_client'], id_chambre=data['id_chambre'], date_arrivee=data['date_arrivee'], date_depart=data['date_depart'], statut="confirmée"),

  db.session.add_all(getReservation)
  db.session.commit()

  return jsonify({'success': True, 'message': 'Réservation créée avec succès.'})

@reservation.route('/api/reservations/<int:id>', methods=['DELETE'])
def delete_reservation(id):
  """
  Description: Supprimer une reservation.

  Vérifications:
  - Si l'id ne correspond à aucunes reservations (#*1)

  Résultat: Réservation annulée avec succès.
  """
  getReservation = Reservation.query.get(id)

  #*1
  if not getReservation:
    return jsonify({'success': False, 'message': 'Réservation inexistante.'})

  getReservation.statut = "annulée"
  db.session.delete(getReservation)
  db.session.commit()

  return jsonify({'success': True, 'message': 'Réservation annulée avec succès.'})

#Route pour afficher toutes les reservations
@reservation.route('/api/reservations/all', methods=['GET'])
def get_all_reservations():
  """
  Description: Afficher toutes les reservations.

  Résultat: Liste de toutes les reservations.
  """
  getAllReservations = Reservation.query.all()
  listAllReservations = []

  for reservation in getAllReservations:
    listAllReservations.append({
      'id': reservation.id,
      'id_client': reservation.id_client,
      'id_chambre': reservation.id_chambre,
      'date_arrivee': reservation.date_arrivee,
      'date_depart': reservation.date_depart,
      'statut': reservation.statut
    })

  return listAllReservations
