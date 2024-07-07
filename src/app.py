"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Character, Vehicle, Planet, Fav_character, Fav_vehicle, Fav_planet
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/users', methods=['GET'])
def all_users():

    users = User.query.all()
    users_serialized = list(map(lambda user: user.serialize(), users))

    response_body = {
        "msg": "Ok",
        "users": users_serialized
    }

    return jsonify(response_body), 200

@app.route('/users/favorites', methods=['GET'])
def all_user_favorites():

    fav_characters = Fav_character.query.all()
    fav_characters_serialized = list(map(lambda favorite: favorite.serialize(), fav_characters))

    fav_vehicles = Fav_vehicle.query.all()
    fav_vehicles_serialized = list(map(lambda favorite: favorite.serialize(), fav_vehicles))

    fav_planets = Fav_planet.query.all()
    fav_planets_serialized = list(map(lambda favorite: favorite.serialize(), fav_planets))

    response_body = {
        "msg": "Ok",
        "favorites characters": fav_characters_serialized,
        "favorites vehicles": fav_vehicles_serialized,
        "favorites planets": fav_planets_serialized
    }

    return jsonify(response_body), 200

@app.route('/users', methods=['POST'])
def create_user():

    body = request.json

    if body is None:
        return "El cuerpo de la solicitud es null", 400
    if 'email' not in body:
        return 'Debes especificar el email', 400
    if 'password' not in body:
        return 'Debes especificar una contraseña', 400
    if 'is_active' not in body:
        return 'Debes especificar si el usuario está activo', 400

    user = User(email = body["email"], password = body["password"], is_active = body["is_active"])
    db.session.add(user)
    db.session.commit()

    response_body = {
        "msg": "Ok",
        "id": user.id
    }

    return jsonify(response_body), 200

@app.route('/people', methods=['GET'])
def all_characters():

    characters = Character.query.all()
    characters_serialized = list(map(lambda character: character.serialize(), characters))

    response_body = {
        "msg": "Ok",
        "characters": characters_serialized
    }

    return jsonify(response_body), 200

@app.route('/people/<int:people_id>', methods=['GET'])
def get_character(people_id):

    character = Character.query.filter_by(id = people_id).first()

    if character:
        character_serialized = character.serialize()

        response_body = {
            "msg": "Ok",
            "character": character_serialized
        }
    else:
        return "Este personaje no existe", 400

    return jsonify(response_body), 200

@app.route('/favorite/people/<int:people_id>', methods=['POST'])
def create_fav_character(people_id):

    character = Character.query.filter_by(id = people_id).first()

    if character:
        fav_character = Fav_character(char_relation = people_id, user_relation = 1)
        db.session.add(fav_character)
        db.session.commit()

        response_body = {
            "msg": "Ok",
            "id": fav_character.id
        }
    else:
        return "Este personaje no existe", 400

    return jsonify(response_body), 200

@app.route('/favorite/people/<int:people_id>', methods=['DELETE'])
def delete_fav_character(people_id):

    character = Character.query.filter_by(id = people_id).first()

    if character:
        fav_character = Fav_character.query.filter_by(char_relation = people_id)
        db.session.delete(fav_character)
        db.session.commit()

        response_body = {
            "msg": "Ok"
        }
    else:
        return "Este personaje no existe", 400

    return jsonify(response_body), 200

@app.route('/vehicle', methods=['GET'])
def all_vehicles():

    vehicles = Vehicle.query.all()
    vehicles_serialized = list(map(lambda vehicle: vehicle.serialize(), vehicles))

    response_body = {
        "msg": "Ok",
        "vehicles": vehicles_serialized
    }

    return jsonify(response_body), 200

@app.route('/vehicle/<int:vehicle_id>', methods=['GET'])
def get_vehicle(vehicle_id):

    vehicle = Vehicle.query.filter_by(id = vehicle_id).first()

    if vehicle:
        vehicle_serialized = vehicle.serialize()

        response_body = {
            "msg": "Ok",
            "vehicle": vehicle_serialized
        }
    else:
        return "Este vehículo no existe", 400

    return jsonify(response_body), 200

@app.route('/favorite/vehicle/<int:vehicle_id>', methods=['POST'])
def create_fav_vehicle(vehicle_id):

    vehicle = Vehicle.query.filter_by(id = vehicle_id).first()

    if vehicle:
        fav_vehicle = Fav_vehicle(vehic_relation = vehicle_id, user_relation = 1)
        db.session.add(fav_vehicle)
        db.session.commit()

        response_body = {
            "msg": "Ok",
            "id": fav_vehicle.id
        }
    else:
        return "Este vehículo no existe", 400

    return jsonify(response_body), 200

@app.route('/favorite/vehicle/<int:vehicle_id>', methods=['DELETE'])
def delete_fav_vehicle(vehicle_id):

    vehicle = Vehicle.query.filter_by(id = vehicle_id).first()

    if vehicle:
        fav_vehicle = Fav_vehicle.query.filter_by(vehic_relation = vehicle_id).first()
        db.session.delete(fav_vehicle)
        db.session.commit()

        response_body = {
            "msg": "Ok"
        }
    else:
        return "Este vehículo no existe", 400

    return jsonify(response_body), 200

@app.route('/planet', methods=['GET'])
def all_planets():

    planets = Planet.query.all()
    planets_serialized = list(map(lambda planet: planet.serialize(), planets))

    response_body = {
        "msg": "Ok",
        "planets": planets_serialized
    }

    return jsonify(response_body), 200

@app.route('/planet/<int:planet_id>', methods=['GET'])
def get_planet(planet_id):

    planet = Planet.query.filter_by(id = planet_id).first()

    if planet:
        planet_serialized = planet.serialize()

        response_body = {
            "msg": "Ok",
            "planet": planet_serialized
        }
    else:
        return "Este planeta no existe", 400

    return jsonify(response_body), 200

@app.route('/favorite/planet/<int:planet_id>', methods=['POST'])
def create_fav_planet(planet_id):

    planet = Planet.query.filter_by(id = planet_id).first()

    if planet:
        fav_planet = Fav_planet(planet_relation = planet_id, user_relation = 1)
        db.session.add(fav_planet)
        db.session.commit()

        response_body = {
            "msg": "Ok",
            "id": fav_planet.id
        }
    else:
        return "Este planeta no existe", 400

    return jsonify(response_body), 200

@app.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
def delete_fav_planet(planet_id):

    planet = Planet.query.filter_by(id = planet_id).first()

    if planet:
        fav_planet = Fav_planet.query.filter_by(planet_relation = planet_id).first()
        db.session.delete(fav_planet)
        db.session.commit()

        response_body = {
            "msg": "Ok"
        }
    else:
        return "Este planeta no existe", 400

    return jsonify(response_body), 200

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
