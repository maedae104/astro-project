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
    phone_number = db.Column(db.String(12), nullable=False)

    # text_update = db.relationship("TextUpdates", back_populates="user")


    def __repr__(self):
            return f'<User: user_id={self.user_id}, Username={self.username}, email={self.email}, phone_number={self.phone_number}, text_update={self.phone_number}>'

class Transit(db.Model):

    __tablename__ = "transits"

    transit_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    date = db.Column(db.DateTime)
    sun_sign = db.Column(db.String)
    moon_sign = db.Column(db.String)
    moon_phase = db.Column(db.String)
    

    # text_update = db.relationship("Transit", back_populates="transit")

    def __repr__(self):
            return f'<Transit: transit_id={self.transit_id}, Date={self.date}, sun_sign={self.sun_sign}, moon_phase={self.moon_phase} moon_sign={self.moon_sign}>'
class TextUpdates(db.Model):

    update_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    transit_date = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))

    # transit = db.relationship("Transit", back_populates="text_update")
    # user = db.relationship("User", back_populates="text_update")



if __name__ == "__main__":
    from server import app

    connect_to_db(app)