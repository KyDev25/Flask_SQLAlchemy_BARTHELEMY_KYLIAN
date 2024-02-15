from flask import Blueprint, request, jsonify
from ..models import Chambre, Reservation
from ..database import db
from datetime import datetime

chambre = Blueprint('chambre', __name__)

#Route pour créer une chambre
@chambre.route('/api/chambres', methods=['POST'])
def add_room():
  data = request.get_json()
  getRoom = Chambre.query.filter_by(numero=data['numero']).first()

  #S'il n'y a pas de paramètres dans le body
  if not data:
    return jsonify({'success': False, 'message': 'Chambre non créee.'})

  #Si le numéro de chambre existe déjà
  if getRoom:
    return jsonify({'success': False, 'message': 'Chambre déjà existante.'})

  getRoom = Chambre(numero=data['numero'], type=data['type'], prix=data['prix']),

  db.session.add_all(getRoom)
  db.session.commit()

  return jsonify({'success': True, 'message': 'Chambre créée avec succès.'})

#Route pour modifier une chambre
@chambre.route('/api/chambres/<int:id>', methods=['PUT'])
def modify_room(id):
  data = request.get_json()
  getRoom = Chambre.query.get(id)

  #S'il n'y a pas de paramètres dans le body
  if not data:
    return jsonify({'success': False, 'message': 'Chambre inexistante.'})

  #Si le numéro de chambre existe déjà
  if not getRoom:
    return jsonify({'success': False, 'message': 'Chambre inexistante.'})

  #Vérification des champs qui ont été modifiés
  if data['numero']:
    getNumberRoom = Chambre.query.filter_by(numero=data['numero']).first()
    #Si le numéro de chambre existe déjà
    if getNumberRoom:
      return jsonify({'success': False, 'message': 'Chambre déjà existante.'})
    getRoom.numero = data['numero']
  if data['type']:
    getRoom.type = data['type']
  if data['prix']:
    getRoom.prix = data['prix']

  db.session.commit()

  return jsonify({'success': True, 'message': 'Chambre mise à jour avec succès.'})

@chambre.route('/api/chambres/<int:id>', methods=['DELETE'])
def delete_room(id):
  getRoom = Chambre.query.get(id)

  #Si l'id ne correspond à aucunes chambres
  if not getRoom:
    return jsonify({'success': False, 'message': 'Chambre inexistante.'})

  db.session.delete(getRoom)
  db.session.commit()

  return jsonify({'success': True, 'message': 'Chambre annulée avec succès.'})

#Route pour rechercher la dispoibilité des chambres
@chambre.route('/api/chambres/disponibles', methods=['GET'])
def search_disponibility_rooms():
  getRooms = Chambre.query.all()
  data = request.get_json()
  #Liste des chambres filtrées qui ne sont pas disponibles
  listFilterRooms = []
  #Liste finale des chambres disponibles
  listDisponibilitiesRooms = []
  arrival_date = datetime.strptime(data['date_arrivee'],'%Y-%m-%d')
  departure_date = datetime.strptime(data['date_depart'],'%Y-%m-%d')

  #On parcours la liste de toutes les chambres
  for room in getRooms:
        #On récupère toutes les réservations d'une seule chambre
        getReservations = Reservation.query.filter_by(id_chambre=room.id).all()
        #On parcours la liste de toutes les réservations de la chambre
        for reservation in getReservations:
          # Si la date d'arrivee ou la date de depart est comprise dans l'intervalle
          if ((arrival_date <= reservation.date_depart <= departure_date) or (arrival_date <= reservation.date_arrivee <= departure_date)) or ((arrival_date == reservation.date_depart and departure_date == reservation.date_depart) or (arrival_date == reservation.date_arrivee and departure_date == reservation.date_arrivee)):
            listFilterRooms.append(room)
        if room not in listFilterRooms:
          listDisponibilitiesRooms.append({'id': room.id, 'numero': room.numero, 'type': room.type, 'prix': room.prix})

  return listDisponibilitiesRooms

#Route pour afficher toutes les chambres
@chambre.route('/api/chambres/all', methods=['GET'])
def get_all_chambres():
  getAllChambres = Chambre.query.all()
  listAllChambres = []

  for chambre in getAllChambres:
    listAllChambres.append({
      'id': chambre.id,
      'numero': chambre.numero,
      'type': chambre.type,
      'prix': chambre.prix
    })

  return listAllChambres
