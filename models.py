from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User (db.Model):
    __tablename__ = "user"
    id = db.Column (db.Integer, primary_key=True)
    name = db.Column (db.String(100), nullable=False)

    def serialize(self):
        return{
            "id": self.id,
            "name": self.name
        }