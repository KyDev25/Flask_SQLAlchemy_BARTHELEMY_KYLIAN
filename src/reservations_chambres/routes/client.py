from flask import Blueprint, request, jsonify
from ..models import Client
from ..database import db

client = Blueprint('client', __name__)

@client.route('/api/clients', methods=['POST'])
def add_client():
  """
  Description: Créer un nouveau client.

  Vérifications:
  - S'il n'y a des paramètres dans le body (#*1)

  Résultat: Client créé avec succès.
  """
  data = request.get_json()

  #*1
  if not data:
    return jsonify({'success': False, 'message': 'Client non créé.'})

  getClient = Client(nom=data['nom'], email=data['email']),

  db.session.add_all(getClient)
  db.session.commit()

  return jsonify({'success': True, 'message': 'Client créé avec succès.'})

#Route pour modifier un client
@client.route('/api/clients/<int:id>', methods=['PUT'])
def modify_client(id):
  """
  Description: Modifier un client.

  Vérifications:
  - S'il n'y a des paramètres dans le body (#*1)
  - Si l'id ne correspond à aucuns clients (#*2)
  - Si l'uns des champs du paramètre est modifié (#*3)

  Résultat: Client mise à jour avec succès.
  """
  data = request.get_json()
  getClient = Client.query.get(id)

  #*1
  if not data:
    return jsonify({'success': False, 'message': 'Client inexistante.'})

  #*2
  if not getClient:
    return jsonify({'success': False, 'message': 'Client inexistante.'})

  #*3
  if data['nom']:
    getClient.nom = data['nom']
  if data['email']:
    getClient.email = data['email']

  db.session.commit()

  return jsonify({'success': True, 'message': 'Client mise à jour avec succès.'})

#Route pour supprimer un client
@client.route('/api/clients/<int:id>', methods=['DELETE'])
def delete_client(id):
  """
  Description: Supprimer un client.

  Vérifications:
  - Si l'id ne correspond à aucuns clients (#*1)

  Résultat: Client supprimé avec succès.
  """

  getClient = Client.query.get(id)

  #*1
  if not getClient:
    return jsonify({'success': False, 'message': 'Client inexistante.'})

  db.session.delete(getClient)
  db.session.commit()

  return jsonify({'success': True, 'message': 'Client supprimé avec succès.'})

@client.route('/api/clients/all', methods=['GET'])
def get_all_clients():
  """
  Description: Afficher tous les clients.

  Résultat: Liste de tous les clients.
  """
  getAllClients = Client.query.all()
  listAllClients = []

  for client in getAllClients:
    listAllClients.append({
      'id': client.id,
      'nom': client.nom,
      'email': client.email
    })


  return listAllClients
