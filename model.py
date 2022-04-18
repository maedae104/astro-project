from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_to_db(flask_app, db_uri="postgresql:///transits", echo=True):
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    flask_app.config["SQLALCHEMY_ECHO"] = echo
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = flask_app
    db.init_app(flask_app)

    print("Connected to the db!")



class User(db.Model):
"""A user."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.String(25), unique=True)
    email = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(25), nullable=False)


    def __repr__(self):
            return f'<User: user_id={self.user_id}, Username={self.username}, email={self.email}>'

class Transit(db.Model):

    transit_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    date = db.Column(db.DateTime)
    sun_sign = db.Column(db.String)
    moon_sign = db.Column(db.String)
    moon_phase = db.Column(db.String)

class TextUpdates(db.Model):

    update_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    transit_date = db.Column(db.DateTime)
    user_id = db.Column(db.)







if __name__ == "__main__":
    from server import app

    connect_to_db(app)