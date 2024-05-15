from flask import Flask, jsonify, request
from models import db, User, Photos
from flask_migrate import Migrate

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///dataBase.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  
db.init_app(app)
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
    new_photo = Photos(id=data["id"], image=data["image"])
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

if __name__ == "__main__":
    with app.app_context():
        db.create_all()  
    app.run(host="0.0.0.0", port="5000", debug=True)



