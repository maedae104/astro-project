
def get_sun_sign():
    curl -X GET http://cerridwen.bluemagician.vc/api/v1/sun


def get_moon_sign():

def get_moon_phase():


def create_user(email, password):
    """Create and return a new user."""

    user = User(email=email, password=password)

    return user

def check_user_email(x_email):
    
    return User.query.filter(User.email == x_email).first()

def get_user_password(x_email, x_password):

    x_user = User.query.filter(User.email == x_email).first()   
    return x_user.password

