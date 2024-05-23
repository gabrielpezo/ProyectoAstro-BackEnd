from flask import Flask, jsonify, request
from models import db, User, Photos, Comments, Categories, Cart, CartItem, Photographer, Favourites
from flask_migrate import Migrate
from flask_cors import CORS

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///dataBase.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
CORS(app)
migrate = Migrate(app, db)

@app.route('/users', methods=['GET'])
def handle_get_all_users():
    users = User.query.all()
    users_list = [user.serialize() for user in users]
    return jsonify({"msg": "success", "users": users_list}), 200

@app.route("/users/<int:id>", methods=["GET"])
def handle_get_user(id):
    user = User.query.get_or_404(id)
    return jsonify(user.serialize()), 200

@app.route("/users", methods=["POST"])
def handle_create_user():
    data = request.get_json()
    new_user = User(name=data["name"], email=data["email"], password=data["password"])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"msg": "success", "user": new_user.serialize()}), 201

@app.route("/users/<int:id>", methods=["PUT"])
def update_user(id):
    data = request.get_json()
    user = User.query.get_or_404(id)
    user.name = data.get("name", user.name)
    user.email = data.get("email", user.email)
    user.password = data.get("password", user.password)
    db.session.commit()
    return jsonify({"msg": "user updated", "user": user.serialize()}), 200

@app.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({"msg": "User was deleted"}), 200

@app.route('/photos', methods=['GET'])
def handle_get_all_photos():
    photos = Photos.query.all()
    photos_list = [photo.serialize() for photo in photos]
    return jsonify({"msg": "success", "photos": photos_list}), 200

@app.route('/photos/<int:id>', methods=['GET'])
def handle_get_photo(id):
    photo = Photos.query.get_or_404(id)
    return jsonify(photo.serialize()), 200

@app.route('/photos', methods=['POST'])
def handle_create_photo():
    data = request.get_json()
    new_photo = Photos(
        name=data["name"],
        price=data["price"],
        rating=data["rating"],
        reviews=data["reviews"],
        likes=data["likes"],
        image=data["image"]
    )
    db.session.add(new_photo)
    db.session.commit()
    return jsonify({"msg": "success", "photo": new_photo.serialize()}), 201

@app.route('/photos/<int:id>', methods=['PUT'])
def handle_update_photo(id):
    data = request.get_json()
    photo = Photos.query.get_or_404(id)
    photo.image = data.get("image", photo.image)
    db.session.commit()
    return jsonify({"msg": "photo updated", "photo": photo.serialize()}), 200

@app.route('/photos/<int:id>', methods=['DELETE'])
def handle_delete_photo(id):
    photo = Photos.query.get_or_404(id)
    db.session.delete(photo)
    db.session.commit()
    return jsonify({"msg": "Photo was deleted"}), 200

@app.route('/cart/<int:user_id>', methods=['GET'])
def get_cart(user_id):
    cart = Cart.query.filter_by(user_id=user_id).first()
    if not cart:
        return jsonify({'message': 'Cart not found'}), 404
    
    return jsonify(cart.serialize())

@app.route('/cart/<int:user_id>/add', methods=['POST'])
def add_to_cart(user_id):
    data = request.json
    photo_id = data['photo_id']
    quantity = data.get('quantity', 1)

    cart = Cart.query.filter_by(user_id=user_id).first()
    if not cart:
        cart = Cart(user_id=user_id, date='today')
        db.session.add(cart)
        db.session.commit()

    cart_item = CartItem.query.filter_by(cart_id=cart.id, photo_id=photo_id).first()
    if cart_item:
        cart_item.quantity += quantity
    else:
        cart_item = CartItem(cart_id=cart.id, photo_id=photo_id, quantity=quantity)
        db.session.add(cart_item)
    
    db.session.commit()
    return jsonify({'message': 'Product added to cart'})


if __name__ == "__main__":
    with app.app_context():
        db.create_all()  
    app.run(host="0.0.0.0", port="5000", debug=True)



