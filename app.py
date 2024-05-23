from flask import Flask, jsonify, request
from models import db, User, Photos, Comments, Categories, Cart, Photographer, Favourites
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
    new_photo = Photos()
    new_photo.name = data["name"]
    new_photo.price = data["price"]
    new_photo.rating = data["rating"]
    new_photo.reviews = data["reviews"]
    new_photo.likes = data["likes"]
    new_photo.image = data["image"]
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

from flask import request, jsonify

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


# @app.route('/photographer', methods=['POST'])
# def create_photographer():
#     data = request.get_json()
#     required_fields = ['name', 'email', 'password', 'photographer_info', 'photo_name', 'photo_price', 'photo_image']

#     if not data or not all(field in data for field in required_fields):
#         return jsonify({"error": "Missing required data, please include: " + ", ".join(required_fields)}), 400

#     try:
#         new_photo = Photos(
#             name=data['photo_name'],
#             price=data['photo_price'],
#             image=data['photo_image'],
#             rating=0,  
#             reviews=0,  
#             likes=0    
#         )
#         db.session.add(new_photo)
#         db.session.flush()  # Para obtener el ID inmediatamente después de insertar

#         new_photographer = Photographer(
#             name=data['name'],
#             email=data['email'],
#             password=data['password'],
#             photographer_info=data['photographer_info'],
#             photos_id=new_photo.id
#         )
#         db.session.add(new_photographer)
#         db.session.commit()

#         return jsonify(new_photographer.serialize()), 201
#     except Exception as e:
#         db.session.rollback()
#         return jsonify({"error": str(e)}), 500

# class Photographer(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(120), nullable=False)
#     photo = db.Column(db.String(300), nullable=True)
#     about_me = db.Column(db.String(300), nullable=True)

# @app.route('/photographer/<int:id>', methods=['GET'])
# def get_photographer(id):
#     photographer = Photographer.query.get_or_404(id)
#     return jsonify({
#         'name': photographer.name,
#         'photo': photographer.photo,
#         'aboutMe': photographer.about_me
#     })

# @app.route('/photographer/<int:id>', methods=['PUT'])
# def update_photographer(id):
#     photographer = Photographer.query.get(id)
#     if not photographer:
#         return jsonify({"error": "Photographer not found"}), 404

#     data = request.json
#     photographer.name = data.get('name', photographer.name)
#     photographer.email = data.get('email', photographer.email)
#     photographer.photographer_info = data.get('photographer_info', photographer.photographer_info)

#     # Si también deseas actualizar la foto asociada, debes manejar eso aquí también
#     if 'photo' in data:
#         photo = Photos.query.get(photographer.photos_id)
#         if photo:
#             photo.image = data['photo'].get('image', photo.image)
#             db.session.commit()

#     db.session.commit()
#     return jsonify(photographer.serialize())

    
# @app.route('/photographer/<int:id>', methods=['DELETE'])
# def delete_photographer(id):
#     photographer = Photographer.query.get(id)
#     if not photographer:
#         return jsonify({"error": "Photographer not found"}), 404

#     db.session.delete(photographer)
#     db.session.commit()
#     return jsonify({"success": "Photographer deleted"})

if __name__ == "__main__":
    with app.app_context():
        print(app.url_map)
        db.create_all()  
    app.run(host="0.0.0.0", port="5000", debug=True)

