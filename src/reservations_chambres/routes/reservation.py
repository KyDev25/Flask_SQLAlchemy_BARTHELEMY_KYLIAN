from flask import Blueprint, request, jsonify
from ..models import Chambre, Reservation
from ..database import db
from datetime import datetime

reservation = Blueprint('reservation', __name__)

#Route pour créer une reservation
@reservation.route('/api/reservations', methods=['POST'])
def add_reservation():
  data = request.get_json()
  getAllReservations = Reservation.query.join(Chambre).filter(Chambre.id == data['id_chambre']).all()
  arrival_date = datetime.strptime(data['date_arrivee'],'%Y-%m-%d')
  departure_date = datetime.strptime(data['date_depart'],'%Y-%m-%d')

  #S'il n'y a pas de paramètres dans le body
  if not data:
    return jsonify({'success': False, 'message': 'Réservation non créée'})

  #On parcours la liste de toutes les réservations
  for reservation in getAllReservations:
    #Si la date d'arrivee ou la date de depart est comprise dans l'intervalle
    if ((arrival_date <= reservation.date_depart <= departure_date) or (arrival_date <= reservation.date_arrivee <= departure_date)) or ((arrival_date == reservation.date_depart and departure_date == reservation.date_depart) or (arrival_date == reservation.date_arrivee and departure_date == reservation.date_arrivee)):
      return jsonify({'success': False, 'message': 'Cette Chambre est déjà réservée dans cet intervalle de temps.'})

  getReservation = Reservation(id_client=data['id_client'], id_chambre=data['id_chambre'], date_arrivee=data['date_arrivee'], date_depart=data['date_depart'], statut="confirmée"),

  db.session.add_all(getReservation)
  db.session.commit()

  return jsonify({'success': True, 'message': 'Réservation créée avec succès.'})

#Route pour supprimer une reservation
@reservation.route('/api/reservations/<int:id>', methods=['DELETE'])
def delete_reservation(id):
  getReservation = Reservation.query.get(id)

  #Si l'id ne correspond à aucunes réservations
  if not getReservation:
    return jsonify({'success': False, 'message': 'Réservation inexistante.'})

  getReservation.statut = "annulée"
  db.session.delete(getReservation)
  db.session.commit()

  return jsonify({'success': True, 'message': 'Réservation annulée avec succès.'})

#Route pour afficher toutes les reservations
@reservation.route('/api/reservations/all', methods=['GET'])
def get_all_reservations():
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
