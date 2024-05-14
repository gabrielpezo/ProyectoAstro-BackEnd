from flask import Flask, jsonify, request
from models import db, User
from flask_migrate import Migrate



app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///dataBase.db"
db.init_app(app)
migrate = Migrate(app, db)

@app.route('/get_users', methods=['GET'])
def handle_get_all_users():
    handle_get_all_users = User().query.all()
    get_all_users = list(map(lambda user:user.serialize(), handle_get_all_users))
    return jsonify({"msg": "success", "users": get_all_users}), 200

@app.route("/get_users/<int:id>", methods=["GET"])
def handle_get_user(id):
    get_user = User.query.get_or_404(id)  
    return jsonify(get_user.serialize()), 200

@app.route("/create_user", methods=["POST"])
def handle_user():
    data = request.get_json()
    create_user = User()
    create_user.name = data["name"]

    db.session.add (create_user)
    db.session.commit() 
    return jsonify({"msg": "success", "data":data}), 201

@app.route("/get_users/<int:id>", methods=["PUT"])
def update_user(id):
    data = request.get_json()
    update_user = User().query.filter_by(id=id).first()
    if update_user is not None:
        update_user.name = data["name"]
        db.session.commit()
        return jsonify({"msg": "user upgraded", "user": update_user.serialize()}), 200
    else:
        return jsonify({"msg": "user not found"}), 404

@app.route('/get_users/<int:id>', methods=['DELETE'])
def delete_user(id):
    get_user = User.query.get_or_404(id)
    db.session.delete(get_user)
    db.session.commit()
    return jsonify({"msg": "User was deleted"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000", debug=True)
