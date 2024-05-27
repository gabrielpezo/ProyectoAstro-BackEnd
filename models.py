from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    email = db.Column(db.String(250), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    carts = db.relationship('Cart', backref='user', lazy=True)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email
        }
    #falta
class Photos(db.Model):
    __tablename__ = 'photos'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    price = db.Column(db.Float, nullable=False)
    rating = db.Column(db.Float, nullable=False)
    reviews = db.Column(db.Integer, nullable=False)
    likes = db.Column(db.Integer, nullable=False)
    image = db.Column(db.String(250), nullable=False)
    categories = db.relationship('Categories', backref='photo', lazy=True)
    cart_items = db.relationship('CartItem', backref='product', lazy=True)

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
     #mejora posible 
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
    #mejora posible 
class Categories (db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    description = db.Column(db.String(1000), nullable=False)
    photo_id = db.Column(db.Integer, db.ForeignKey('photos.id'))

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "photo_id": self.photo_id
        }

class Cart(db.Model):
    __tablename__ = 'cart'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(20), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    items = db.relationship('CartItem', backref='cart', lazy=True)

    def serialize(self): 
        return {
            "id": self.id,
            "date": self.date,
            "user_id": self.user_id,
            "items": [item.serialize() for item in self.items]
        }

class CartItem(db.Model):
    __tablename__ = 'cart_item'
    id = db.Column(db.Integer, primary_key=True)
    cart_id = db.Column(db.Integer, db.ForeignKey('cart.id'), nullable=False)
    photo_id = db.Column(db.Integer, db.ForeignKey('photos.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    total_amount= db.Column(db.Integer, nullable=False, default=0)

    # Relación con la clase Photos
    photo = db.relationship('Photos', foreign_keys=[photo_id])

    def serialize(self):
        return {
            "id": self.id,
            "cart_id": self.cart_id,
            "photo_id": self.photo_id,
            "photo_name": self.photo.name,  # Nombre del producto
            "photo_price": self.photo.price,  # Precio del producto
            "quantity": self.quantity,
            "total_amount": self.total_amount,
        }
    
class Photographer(db.Model):
    __tablename__ = 'photographer'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    email = db.Column(db.String(250), unique=True, nullable=False)
    password = db.Column(db.String(250), nullable=False)
    about_me = db.Column(db.String(1000), nullable=False)
    profile_pic = db.Column(db.String(250), unique=True, nullable=False)
    photos_id = db.Column(db.Integer, db.ForeignKey('photos.id'))
    uploaded_photos = db.relationship(Photos, uselist=False)

    def serialize(self):
        return { 
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "about_me": self.about_me,
            "profile_pic": self.profile_pic,
            "photo_id": self.uploaded_photos.id if self.uploaded_photos else None
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
    photo_id = db.Column(db.Integer, db.ForeignKey('photos.id'))

    def serialize(self):
        return {
            "id": self.id,
            "photographer_id": self.photographer_id,
            "photo_id": self.photo_id
        }
