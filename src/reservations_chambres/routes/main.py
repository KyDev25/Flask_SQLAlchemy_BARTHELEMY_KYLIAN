from flask import Blueprint

main = Blueprint('main', __name__)

@main.route('/api', methods=['POST', 'DELETE', 'UPDATE', 'GET'])
def index():
  return "Réservations de Chambres"
