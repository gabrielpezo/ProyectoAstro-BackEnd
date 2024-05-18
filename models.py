
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

# def init_db():
#     try:
#         with app.app_context():
#             db.create_all()
#             if not Photos.query.all():
#                 db.session.add_all([
#                     Photos(id=1, name="Fotografía Astro", price=100.00, rating=4.8, reviews=67, likes=200, image="https://picsum.photos/id/26/600/800"),
#                     Photos(id=2, name="Producto 2", price=50.00, rating=2.5, reviews=6, likes=2, image="https://picsum.photos/id/27/600/800"),
#                     Photos(id=3, name="Producto 3", price=60.00, rating=3.5, reviews=621, likes=322, image="https://picsum.photos/id/28/600/800"),
#                     Photos(id=4, name="Producto 4", price=40.00, rating=4.5, reviews=43, likes=223, image="https://picsum.photos/id/29/600/800"),
#                     Photos(id=5, name="Producto 5", price=255.00, rating=3.5, reviews=323, likes=211, image="https://picsum.photos/id/30/600/800"),
#                     Photos(id=6, name="Producto 6", price=5.530, rating=4.9, reviews=453, likes=222, image="https://picsum.photos/id/31/600/800")
#                 ])
#                 db.session.commit()
#     except Exception as e:
#         print("Error initializing database:", e)

# # Llamar a la función init_db() para inicializar la base de datos
# init_db()
