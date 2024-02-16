from flask import Blueprint, request, jsonify
from ..models import Chambre, Reservation
from ..database import db
from datetime import datetime

chambre = Blueprint('chambre', __name__)

@chambre.route('/api/chambres', methods=['POST'])
def add_room():
  """
  Description: Créer une nouvelle chambre.

  Vérifications:
  - S'il n'y a des paramètres dans le body (#*1)
  - Si le numéro de chambre existe déjà (#*2)

  Résultat: Chambre créée avec succès.
  """
  data = request.get_json()
  getRoom = Chambre.query.filter_by(numero=data['numero']).first()

  #*1
  if not data:
    return jsonify({'success': False, 'message': 'Chambre non créee.'})

  #*2
  if getRoom:
    return jsonify({'success': False, 'message': 'Chambre déjà existante.'})

  getRoom = Chambre(numero=data['numero'], type=data['type'], prix=data['prix']),

  db.session.add_all(getRoom)
  db.session.commit()

  return jsonify({'success': True, 'message': 'Chambre créée avec succès.'})

@chambre.route('/api/chambres/<int:id>', methods=['PUT'])
def modify_room(id):
  """
  Description: Modifier une chambre.

  Vérifications:
  - S'il n'y a des paramètres dans le body (#*1)
  - Si l'id ne correspond à aucunes chambres (#*2)
  - Si l'uns des champs du paramètre est modifié (#*3)
  - Si le numéro de chambre existe déjà (#*4)

  Résultat: Chambre mise à jour avec succès.
  """
  data = request.get_json()
  getRoom = Chambre.query.get(id)

  #*1
  if not data:
    return jsonify({'success': False, 'message': 'Chambre inexistante.'})

  #*2
  if not getRoom:
    return jsonify({'success': False, 'message': 'Chambre inexistante.'})

  #*3
  if data['numero']:
    getNumberRoom = Chambre.query.filter_by(numero=data['numero']).first()
    #*4
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
  """
  Description: Supprimer une chambre.

  Vérifications:
  - Si l'id ne correspond à aucunes chambres (#*1)

  Résultat: Chambre supprimée avec succès.
  """
  getRoom = Chambre.query.get(id)

  #*1
  if not getRoom:
    return jsonify({'success': False, 'message': 'Chambre inexistante.'})

  db.session.delete(getRoom)
  db.session.commit()

  return jsonify({'success': True, 'message': 'Chambre supprimée avec succès.'})

@chambre.route('/api/chambres/disponibles', methods=['GET'])
def search_disponibility_rooms():
  """
  Description: Rechercher la disponibilité des chambres.

  Vérifications:
  - Si la date d'arrivee ou la date de depart est comprise dans l'intervalle (#*1)
  - Si la chambre fait partie des chambres indisponibles (#*2)

  Etapes:
  - On recupère toutes les chambres (#*3)
  - On récupère toutes les réservations d'une chambre (#*4)
  - On parcours la liste de toutes les chambres (#*5)

  Résultat: Liste des chambres disponibles.
  """
  getRooms = Chambre.query.all()
  data = request.get_json()
  #Liste des chambres filtrées qui ne sont pas disponibles
  listFilterRooms = []
  #Liste finale des chambres disponibles
  listDisponibilitiesRooms = []
  arrival_date = datetime.strptime(data['date_arrivee'],'%Y-%m-%d')
  departure_date = datetime.strptime(data['date_depart'],'%Y-%m-%d')

  if arrival_date > departure_date:
    return jsonify({'success': False, 'message': 'La date d\'arrivée doit être inferieure à la date de départ'})

  #*3
  for room in getRooms:
        #*4
        getReservations = Reservation.query.filter_by(id_chambre=room.id).all()
        #*5
        for reservation in getReservations:
          #*1
          if ((arrival_date <= reservation.date_depart <= departure_date) or (arrival_date <= reservation.date_arrivee <= departure_date)) or ((arrival_date == reservation.date_depart and departure_date == reservation.date_depart) or (arrival_date == reservation.date_arrivee and departure_date == reservation.date_arrivee)):
            listFilterRooms.append(room)
        #*2
        if room not in listFilterRooms:
          listDisponibilitiesRooms.append({'id': room.id, 'numero': room.numero, 'type': room.type, 'prix': room.prix})

  return listDisponibilitiesRooms

#Route pour afficher toutes les chambres
@chambre.route('/api/chambres/all', methods=['GET'])
def get_all_chambres():
  """
  Description: Afficher toutes les chambres.

  Résultat: Liste de toutes les chambres.
  """
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
