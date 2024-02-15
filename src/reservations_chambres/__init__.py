from flask import Flask
from flask_migrate import Migrate
from .models import Client
from .database import db

migrate = Migrate()

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = "mysecretkey"
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:pass@db/reservations_chambres'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    migrate.init_app(app, db)

    from .routes.main import main
    app.register_blueprint(main)

    from .routes.reservation import reservation
    app.register_blueprint(reservation)

    from .routes.chambre import chambre
    app.register_blueprint(chambre)

    from .routes.client import client
    app.register_blueprint(client)

    return app
