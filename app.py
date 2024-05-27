from datetime import timedelta
from flask import Flask, jsonify, request
from models import db, User, Photos, Comments, Categories, Cart, CartItem, Photographer, Favourites
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

expires_jwt = timedelta(minutes=1000)


@app.route('/get_users', methods=['GET'])
@jwt_required()
def handle_get_all_users():
    users = User.query.all()
    users_list = [user.serialize() for user in users]
    return jsonify({"msg": "success", "users": users_list}), 200

@app.route("/users/<int:id>", methods=["GET"])
def handle_get_user(id):
    user = User.query.get_or_404(id)
    return jsonify(user.serialize()), 200

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


@app.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    user = User.query.get_or_404(id)
    db.session.delete(user)
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
    photo.likes = data.get("likes", photo.likes)
    photo.name = data.get("name", photo.name)
    photo.price = data.get("price", photo.price)
    photo.rating = data.get("rating", photo.rating)
    photo.reviews = data.get("reviews", photo.reviews)
    db.session.commit()
    return jsonify({"msg": "photo updated", "photo": photo.serialize()}), 200

@app.route('/photos/<int:id>', methods=['DELETE'])
def handle_delete_photo(id):
    photo = Photos.query.get_or_404(id)
    db.session.delete(photo)
    db.session.commit()
    return jsonify({"msg": "Photo was deleted"}), 200


@app.route('/photographer', methods=['POST'])
def add_photographer():
    data = request.get_json()
    try:
        new_photographer = Photographer(
            name=data['name'],
            email=data['email'], 
            password=data['password'],
            about_me=data['about_me'],
            profile_pic=data['profile_pic']
        )
        db.session.add(new_photographer)
        db.session.commit()
        return jsonify(new_photographer.serialize()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400

@app.route('/photographers', methods=['GET'])
def get_all_photographers():
    photographers = Photographer.query.all()
    photographers_data = [{
        "id": photographer.id,
        "name": photographer.name,
        "email": photographer.email,
        "about_me": photographer.about_me,
        "profile_pic": photographer.profile_pic
    } for photographer in photographers]

    return jsonify(photographers_data)


@app.route('/photographer/<int:id>', methods=['PUT'])
def update_photographer(id):
    photographer = Photographer.query.get(id)
    if not photographer:
        return jsonify({"error": "Photographer not found"}), 404

    data = request.get_json()
    try:
        if 'name' in data:
            photographer.name = data['name']
        if 'email' in data:
            photographer.email = data['email']
        if 'password' in data:
            photographer.password = data['password']
        if 'about_me' in data:
            photographer.about_me = data['about_me']
        if 'profile_pic' in data:
            photographer.profile_pic = data['profile_pic']

        db.session.commit()
        return jsonify(photographer.serialize()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400

@app.route('/photographer/<int:id>', methods=['DELETE'])
def delete_photographer(id):
    photographer = Photographer.query.get(id)
    if not photographer:
        return jsonify({"error": "Photographer not found"}), 404

    try:
        db.session.delete(photographer)
        db.session.commit()
        return jsonify({"message": "Photographer deleted successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400
    
@app.route('/profile/<int:id>', methods=['GET'])
def get_photographer_profile(id):
    photographer = Photographer.query.get(id)
    if not photographer:
        return jsonify({"error": "Photographer not found"}), 404

    photographer_data = {
        "name": photographer.name,
        "about_me": photographer.about_me,
        "profile_pic": photographer.profile_pic 
    }
    return jsonify(photographer_data)


# @app.route('/cart/<int:user_id>', methods=['GET'])
# def get_cart(user_id):
#     cart = Cart.query.filter_by(user_id=user_id).first()
#     if not cart:
#         return jsonify({'message': 'Cart not found'}), 404
    
#     return jsonify(cart.serialize())


# @app.route('/getcartitem/<int:user_id>', methods=['GET'])
# def get_cart_item(user_id):
#     cart = CartItem.query.filter_by(id=user_id).first()
#     if not cart:
#         return jsonify({'message': 'Cart not found'}), 404
    
#     return jsonify(cart.serialize())


@app.route('/cart/add', methods=['POST'])
@jwt_required()  # Proteger el endpoint con JWT, el token debe ser válido para acceder
def add_to_cart():
    current_user = get_jwt_identity()  # Obtener la identidad del usuario desde el token JWT
    user_id = current_user  # current_user ya es el ID del usuario
    data = request.json
    photo_id = data['photo_id']
    quantity = data.get('quantity', 1)

    # Obtener el precio del producto
    photo = Photos.query.get(photo_id)
    if not photo:
        return jsonify({'message': 'Photo not found'}), 404
    
    price = photo.price
    total_amount = price * quantity

    cart = Cart.query.filter_by(user_id=user_id).first()
    if not cart:
        cart = Cart(user_id=user_id, date='today')
        db.session.add(cart)
        db.session.commit()

    cart_item = CartItem.query.filter_by(cart_id=cart.id, photo_id=photo_id).first()
    if cart_item:
        cart_item.quantity += quantity
        cart_item.total_amount += total_amount  # Actualizar el total_amount
    else:
        cart_item = CartItem(cart_id=cart.id, photo_id=photo_id, quantity=quantity, total_amount=total_amount, photo_name=photo.name, photo_price=photo.price)
        db.session.add(cart_item)

    
    db.session.commit()
    
    # Obtener todos los elementos del carrito después de la actualización
    cart_items = CartItem.query.filter_by(cart_id=cart.id).all()
    
    # Serializar los elementos del carrito para incluirlos en la respuesta
    cart_items_data = [{
        "id": item.id,
        "cart_id": item.cart_id,
        "photo_id": item.photo_id,
        "photo_name": item.photo_name,  # Nombre del producto
        "photo_price": item.photo_price,  # Precio del producto
        "quantity": item.quantity,
    } for item in cart_items]

    
    return jsonify({'message': 'Product added to cart', 'cart_items': cart_items_data})


@app.route('/cartuser', methods=['GET'])
@jwt_required()  # Requiere que el usuario esté autenticado
def get_cart():
    try:
        # Obtener la identidad del usuario desde el token JWT
        current_user = get_jwt_identity()
        user_id = current_user  # current_user ya es el ID del usuario

        # Obtener el carrito del usuario
        cart = Cart.query.filter_by(user_id=user_id).first()
        if not cart:
            return jsonify({'message': 'No cart found for this user'}), 404

        # Obtener todos los elementos del carrito para el carrito dado
        cart_items = CartItem.query.filter_by(cart_id=cart.id).all()

        if not cart_items:
            return jsonify({'message': 'No items found in cart'}), 404

        # Serializar los elementos del carrito
        cart_items_data = [{
            "id": item.id,
            "cart_id": item.cart_id,
            "photo_id": item.photo_id,
            "photo_name": item.photo_name,
            "photo_price": item.photo_price,
            "quantity": item.quantity,
            "total_amount": item.total_amount  # Añadir total_amount
        } for item in cart_items]

        return jsonify({'cart_items': cart_items_data}), 200

    except Exception as e:
        print(f"Error: {e}")  # Log the error for debugging
        return jsonify({'error': 'Internal Server Error'}), 500


if __name__ == "__main__":
    with app.app_context():
        print(app.url_map)
        db.create_all()  
    app.run(host="0.0.0.0", port="5000", debug=True)


