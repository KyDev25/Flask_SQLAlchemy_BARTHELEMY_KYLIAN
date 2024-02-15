from flask import Blueprint, request, jsonify
from ..models import Client
from ..database import db

client = Blueprint('client', __name__)

#Route pour créer un client
@client.route('/api/clients', methods=['POST'])
def add_client():
  data = request.get_json()

  #S'il n'y a pas de paramètres dans le body
  if not data:
    return jsonify({'success': False, 'message': 'Client non créé.'})

  getClient = Client(nom=data['nom'], email=data['email']),

  db.session.add_all(getClient)
  db.session.commit()

  return jsonify({'success': True, 'message': 'Client créé avec succès.'})

#Route pour modifier un client
@client.route('/api/clients/<int:id>', methods=['PUT'])
def modify_client(id):
  data = request.get_json()
  getClient = Client.query.get(id)

  if not data:
    return jsonify({'success': False, 'message': 'Client inexistante.'})

  if not getClient:
    return jsonify({'success': False, 'message': 'Client inexistante.'})

  if data['nom']:
    getClient.nom = data['nom']
  if data['email']:
    getClient.email = data['email']

  db.session.commit()

  return jsonify({'success': True, 'message': 'Client mise à jour avec succès.'})

#Route pour supprimer un client
@client.route('/api/clients/<int:id>', methods=['DELETE'])
def delete_client(id):
  getClient = Client.query.get(id)

  #Si l'id ne correspond à aucuns clients
  if not getClient:
    return jsonify({'success': False, 'message': 'Client inexistante.'})

  db.session.delete(getClient)
  db.session.commit()

  return jsonify({'success': True, 'message': 'Client annulée avec succès.'})

#Route pour afficher tous les clients
@client.route('/api/clients/all', methods=['GET'])
def get_all_clients():
  getAllClients = Client.query.all()
  listAllClients = []

  for client in getAllClients:
    listAllClients.append({
      'id': client.id,
      'nom': client.nom,
      'email': client.email
    })


  return listAllClients
