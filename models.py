
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

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
    name = db.Column(db.String(250), nullable=False)
    price = db.Column(db.Float, nullable=False)
    rating = db.Column(db.Float, nullable=False)
    reviews = db.Column(db.Integer, nullable=False)
    likes = db.Column(db.Integer, nullable=False)
    image = db.Column(db.String(250), nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "price": self.price,
            "rating": self.rating,
            "reviews": self.reviews,
            "likes": self.likes,
            "image": self.image
        }
    
class Comments (db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    comments = db.Column(db.String(1000), nullable=False)
    complaints = db.Column(db.String(1000), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship(User, uselist=False)

    def serialize(self):
            return{
                "id": self.id,
                "comments": self.comments,
                "complaints": self.complaints,
                "user_id": self.user.name
            }
    
class Categories (db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    description = db.Column(db.String(1000), nullable=False)
    photo_id = db.Column(db.Integer, db.ForeignKey('photos.id'))
    photo = db.relationship(Photos, uselist=False)

    def serialize(self):
            return{
                "id": self.id,
                "name": self.name,
                "description": self.description,
                "photo_id": self.photo.id
            }
    
class Cart(db.Model):
    __tablename__ = 'cart'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(20), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship(User, uselist=False)
    photo_id = db.Column(db.Integer, db.ForeignKey('photos.id'))
    photo = db.relationship(Photos, uselist=False)

    def serialize(self):
            return{
                "id": self.id,
                "date": self.date,
                "user_id": self.user.name,
                "photo_id": self.photo.id
            }

class Photographer(db.Model):
    __tablename__ = 'photographer'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    email = db.Column(db.String (250), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    photos_id = db.Column(db.Integer, db.ForeignKey('photos.id'))
    uploaded_photos = db.relationship (Photos, uselist=False)

    def serialize(self):
            return{
                "id": self.id,
                "name": self.name,
                "email": self.email,
                "photo_id": self.uploaded_photos.id
            }

class Favourites(db.Model):
    __tablename__ = 'favourites'
    id = db.Column(db.Integer, primary_key=True)
    photographer_id = db.Column(db.Integer, db.ForeignKey('photographer.id'))
    photographer = db.relationship(Photographer, uselist=False)
    photo_id = db.Column(db.Integer, db.ForeignKey('photos.id'))
    photo = db.relationship(Photos, uselist=False)

    def serialize(self):
            return{
                "id": self.id,
                "photographer_id": self.photographer.id,
                "photo_id": self.photo.id
            }
