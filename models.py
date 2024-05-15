from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'  # Cambia esto si usas otra base de datos
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    email = db.Column(db.String(250), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email
        }

class Photos(db.Model):
    __tablename__ = 'photos'
    id = db.Column(db.Integer, primary_key=True)
    image = db.Column(db.String(100), nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "image": self.image,
        }

class Photographer(db.Model):
    __tablename__ = 'photographer'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    email = db.Column(db.String(250), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    photos_id = db.Column(db.Integer, db.ForeignKey('photos.id'))
    uploaded_photos = db.relationship("Photos")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "photos_id": self.photos_id
        }

class Favourites(db.Model):
    __tablename__ = 'favourites'
    id = db.Column(db.Integer, primary_key=True)
    photographer_id = db.Column(db.Integer, db.ForeignKey('photographer.id'))
    photographer = db.relationship("Photographer")
    photo_id = db.Column(db.Integer, db.ForeignKey('photos.id'))
    photo = db.relationship("Photos")

    def serialize(self):
        return {
            "id": self.id,
            "photographer_id": self.photographer_id,
            "photo_id": self.photo_id
        }

class FAQ(db.Model):
    __tablename__ = 'faq'
    id = db.Column(db.Integer, primary_key=True)
    questions = db.Column(db.String(500), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    user = db.relationship("User")

    def serialize(self):
        return {
            "id": self.id,
            "questions": self.questions,
            "user_id": self.user_id
        }

class Comments(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    comments = db.Column(db.String(1000), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship("User")

    def serialize(self):
        return {
            "id": self.id,
            "comments": self.comments,
            "user_id": self.user_id
        }

class Cart(db.Model):
    __tablename__ = 'cart'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(20), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship("User")
    photo_id = db.Column(db.Integer, db.ForeignKey('photos.id'))
    photo = db.relationship("Photos")

    def serialize(self):
        return {
            "id": self.id,
            "date": self.date,
            "user_id": self.user_id,
            "photo_id": self.photo_id
        }

class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    description = db.Column(db.String(1000), nullable=False)
    photo_id = db.Column(db.Integer, db.ForeignKey('photos.id'))
    photo = db.relationship("Photos")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "photo_id": self.photo_id
        }

class Followers(db.Model):
    __tablename__ = "followers"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship("User")
    photographer_id = db.Column(db.Integer, db.ForeignKey('photographer.id'))
    photographer = db.relationship("Photographer")

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "photographer_id": self.photographer_id
        }
