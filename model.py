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
    email = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(25), nullable=False)
    phone_number = db.Column(db.String(12), nullable=False)
    

    text_update = db.relationship("TextUpdates", back_populates="user")


    def __repr__(self):
            return f'<User: user_id={self.user_id}, email={self.email}, phonenumber={self.phone_number}>'

class Transit(db.Model):

    __tablename__ = "transits"

    transit_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    date = db.Column(db.String)
    sun_sign = db.Column(db.String)
    moon_sign = db.Column(db.String)
    moon_phase = db.Column(db.String)
    merc_sign = db.Column(db.String)
    venus_sign = db.Column(db.String)
    mars_sign = db.Column(db.String)
    jup_sign = db.Column(db.String)
    sat_sign = db.Column(db.String)
    uran_sign = db.Column(db.String)
    nept_sign = db.Column(db.String)
    pluto_sign = db.Column(db.String)
   
    

    text_update = db.relationship("TextUpdates", back_populates="transit")

    def __repr__(self):
            return f"""Today's Transits: the sun is in: {self.sun_sign},  
            the moon phase is: {self.moon_phase}, the moon is in: {self.moon_sign}, 
            Mercury is in: {self.merc_sign}, Venus is in: {self.venus_sign},
            Mars is in: {self.mars_sign}, Jupiter is in: {self.jup_sign},
            Saturn is in: {self.sat_sign}, Uranus is in: {self.uran_sign}
            Neptune is in: {self.nept_sign}, Pluto is in: {self.pluto_sign}"""

class TextUpdates(db.Model):

    __tablename__ = "updates"

    update_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    transit_date = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    transit_id = db.Column(db.Integer, db.ForeignKey('transits.transit_id'))
   
    user = db.relationship("User", back_populates="text_update")
    transit = db.relationship("Transit", back_populates="text_update")


if __name__ == "__main__":
    from server import app

    connect_to_db(app)