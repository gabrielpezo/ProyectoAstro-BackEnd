from datetime import timedelta
from flask import Flask, jsonify, request
from models import db, User, Photos, Comments, Categories, Cart, Photographer, Favourites
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, get_jwt_identity, jwt_required



app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///dataBase.db"
app.config["SECRET_KEY"] = "MI_PALABRA_SECRETA"
app.config["JWT_SECRET_KEY"] = "MI_PALABRA_SECRETA_JWT"
db.init_app(app)
CORS(app)
bcrypt = Bcrypt(app)
migrate = Migrate(app, db)
jwt =JWTManager(app)

expires_jwt = timedelta(minutes=10)


@app.route('/get_users', methods=['GET'])
@jwt_required()
def handle_get_all_users():
    handle_get_all_users = User().query.all()
    get_all_users = list(map(lambda user:user.serialize(), handle_get_all_users))
    return jsonify({"msg": "success", "users": get_all_users}), 200

@app.route("/get_users/<int:id>", methods=["GET"])
def handle_get_user(id):
    get_user = User.query.get_or_404(id)  
    return jsonify(get_user.serialize()), 200

#inserte email y pasword

@app.route("/create_user", methods=["POST"])
def handle_user():
    data = request.get_json()
    if User.query.filter_by(email=data["email"]).first():
        return jsonify({"msg": "Email already registered"}), 400

    create_user = User(
        name=data["name"],
        email=data["email"],
        password=bcrypt.generate_password_hash(data["password"]).decode('utf-8')
    )
    db.session.add(create_user)
    db.session.commit()
    return jsonify({"msg": "User created successfully", "data": create_user.serialize()}), 201


@app.route("/get_users/<int:id>", methods=["PUT"])#cambiar a update_users
@jwt_required()
def update_user(id):
    
    
    data = request.get_json()
    print (data)
    update_user = User.query.filter_by(id=id).first() 
    print(update_user)
    if update_user is not None:
        update_user.name = data["name"]
        db.session.commit()
        return jsonify({"msg": "user upgraded", "user": update_user.serialize()}), 200
    else:
        return jsonify({"msg": "user not found"}), 404
  

@app.route("/login", methods=['POST'])
def login():
    email = request.json.get("email")
    password = request.json.get("password")

    user_exist = User.query.filter_by(email=email).first()

    if user_exist and bcrypt.check_password_hash(user_exist.password, password):
        token = create_access_token(identity=email, expires_delta=expires_jwt)
        return jsonify({
            "msg": "success",
            "data": user_exist.serialize(),
            "token": token
        }), 200
    return jsonify({
        "msg": "Invalid email or password"
    }), 401


@app.route('/get_users/<int:id>', methods=['DELETE'])
def delete_user(id):
    get_user = User.query.get_or_404(id)
    db.session.delete(get_user)
    db.session.commit()
    return jsonify({"msg": "User was deleted"}), 200

#este es mi aporte 

#endpoint recuperar cuenta o contraseña
@app.route('/recover_password', methods=['POST'])
def recover_password():
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()
    if user:
        # Aquí agregarías la lógica para enviar el correo electrónico con el enlace de recuperación
        return jsonify({"msg": "Password recovery email sent"}), 200
    return jsonify({"msg": "Email not found"}), 404




    

# esto es traido de la nube 

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
    app.run(host="0.0.0.0", port="5000", debug=True)
