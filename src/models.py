from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }
    
class Character(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    eye_color = db.Column(db.String(40), nullable=False)
    hair_color = db.Column(db.String(40), nullable=False)

    def __repr__(self):
        return '<Character %r>' % self.id
    
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "eye_color": self.eye_color,
            "hair_color": self.hair_color
        }
    
class Vehicle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    model = db.Column(db.String(40), nullable=False)

    def __repr__(self):
        return '<Vehicle %r>' % self.id
    
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "model": self.model
        }
    
class Planet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    population = db.Column(db.Integer(), nullable=False)
    climate = db.Column(db.String(40), nullable=False)

    def __repr__(self):
        return '<Planet %r>' % self.id
    
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "population": self.population,
            "climate": self.climate
        }
    
class Fav_character(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    char_relation = db.Column(db.Integer, db.ForeignKey('character.id'), nullable=False)
    user_relation = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return '<Fav_character %r>' % self.id
    
    def serialize(self):
        return {
            "id": self.id,
            "char_relation": self.char_relation,
            "user_relation": self.user_relation
        }
    
class Fav_vehicle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    vehic_relation = db.Column(db.Integer, db.ForeignKey('vehicle.id'), nullable=False)
    user_relation = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return '<Fav_vehicle %r>' % self.id
    
    def serialize(self):
        return {
            "id": self.id,
            "vehic_relation": self.vehic_relation,
            "user_relation": self.user_relation
        }
    
class Fav_planet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    planet_relation = db.Column(db.Integer, db.ForeignKey('planet.id'), nullable=False)
    user_relation = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return '<Fav_planet %r>' % self.id
    
    def serialize(self):
        return {
            "id": self.id,
            "planet_relation": self.planet_relation,
            "user_relation": self.user_relation
        }