import json
import swisseph as swe
import web_scrape
from model import connect_to_db, db, User, Transit, TextUpdates
from datetime import date
from flask_sqlalchemy import SQLAlchemy

swe.set_ephe_path('/usr/share/sweph/ephe')

today = date.today()
c_today = today.strftime("%Y %m %d")
c_today = c_today.split(' ')
year = int(c_today[0])
month = int(c_today[1])
day = int(c_today[2])
current_date = today.strftime("%b%d")
converted_date = swe.julday(year, month, day)


sun_calcs = swe.calc_ut(converted_date, 0)
moon_calcs = swe.calc_ut(converted_date, 1)
merc_calcs = swe.calc_ut(converted_date, 2)

sun_ecl_long = sun_calcs[0][0]
moon_ecl_long = moon_calcs[0][0]
merc_ecl_long = merc_calcs[0][0]

def calculate_sign(ecl_long):
    sign_degrees = ecl_long

    if sign_degrees > 0 and sign_degrees < 30:
        return "Aries"

    elif sign_degrees > 30 and sign_degrees < 60:
        return "Taurus"
    
    elif sign_degrees > 60 and sign_degrees < 90:
        return "Gemini"

    elif sign_degrees > 90 and sign_degrees < 120:
        return "Cancer"

    elif sign_degrees > 120 and sign_degrees < 150:
        return "Leo"

    elif sign_degrees > 150 and sign_degrees < 180:
        return "Virgo"

    elif sign_degrees > 180 and sign_degrees < 210:
        return "Libra"

    elif sign_degrees > 210 and sign_degrees < 240:
        return "Scorpio"

    elif sign_degrees > 240 and sign_degrees < 270:
        return "Sagittarius"

    elif sign_degrees > 270 and sign_degrees < 300:
        return "Capricorn"
    
    elif sign_degrees > 300 and sign_degrees < 330:
        return "Aquarius"

    elif sign_degrees > 330 and sign_degrees < 360:
        return "Pisces"

def get_moon_phase(current_date):
    xmoon_dict = web_scrape.moon_dict
    if current_date in xmoon_dict.keys():
        return xmoon_dict[current_date][0]

def create_user(email, password):
    """Create and return a new user."""

    user = User(email=email, password=password)

    return user

def get_user_by_email(email):
    
    return User.query.filter(User.email == email).first()

def get_user_password(email, password):

    user = User.query.filter(User.email == email).first()   
    return user.password

if __name__ == '__main__':
    from server import app
    connect_to_db(app)