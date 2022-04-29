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
venus_calcs = swe.calc_ut(converted_date, 3)
mars_calcs = swe.calc_ut(converted_date, 4)
jup_calcs = swe.calc_ut(converted_date, 5)
sat_calcs = swe.calc_ut(converted_date, 6)
uran_calcs = swe.calc_ut(converted_date, 7)
nept_calcs = swe.calc_ut(converted_date, 8)
pluto_calcs = swe.calc_ut(converted_date, 9)


sun_ecl_long = sun_calcs[0][0]
moon_ecl_long = moon_calcs[0][0]
merc_ecl_long = merc_calcs[0][0]
venus_ecl_long = venus_calcs[0][0]
mars_ecl_long = mars_calcs[0][0]
jup_ecl_long = jup_calcs[0][0]
sat_ecl_long = sat_calcs[0][0]
uran_ecl_long =uran_calcs[0][0]
nept_ecl_long = nept_calcs[0][0]
pluto_ecl_long = pluto_calcs[0][0]


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

def get_aspects(planet_a, planet_b):
    """get current aspects in the sky"""

    sign_dict= {
        "Aries": 1,
        "Taurus": 2,
        "Gemini": 3,
        "Cancer": 4,
        "Leo": 5,
        "Virgo": 6,
        "Libra": 7,
        "Scorpio": 8,
        "Sagittarius": 9,
        "Capricorn": 10,
        "Aquarius": 11,
        "Pisces": 12
    }
    

    if sign_dict[planet_b] == sign_dict[planet_a]:
        return "conjunct"

    elif sign_dict[planet_b] == sign_dict[planet_a] + 2 or sign_dict[planet_b] == sign_dict[planet_a] + 10:
        return "sextile"

    elif sign_dict[planet_b] == sign_dict[planet_a] + 3 or sign_dict[planet_b] == sign_dict[planet_a] + 9:
        return "square"
    
    elif sign_dict[planet_b] == sign_dict[planet_a] + 4 or sign_dict[planet_b] == sign_dict[planet_a] + 8:
        return "trine"

    elif sign_dict[planet_b] == sign_dict[planet_a] + 6:
        return "opposition"

# transit_list = [sun_sign, moon_sign, merc_sign, venus_sign, mars_sign, jup_sign, sat_sign, uran_sign, nept_sign, pluto_sign]
#     trans_dict = {
#         sun_sign : " the Sun",
#         moon_sign : "the Moon", 
#         merc_sign : "Mercury",
#         venus_sign : "Venus",
#         mars_sign : "Mars",
#         jup_sign : "Jupiter",
#         sat_sign : "Saturn",
#         nept_sign : "Neptune", 
#         pluto_sign : "Pluto" }
    

#     def get_sun_aspects():
#         for trans in transit_list:
#             sun_aspect = crud.get_aspects(transit_list[0], trans)
#             sun_as_str = f"The sun is { sun_aspect } to { trans_dict[trans] } in { trans }"
#             if sun_aspect != None:
#                 print(sun_as_str)

#     def get_moon_aspects():
#         for trans in transit_list:
#             moon_str_list = []
#             moon_aspect = crud.get_aspects(transit_list[1], trans)
#             moon_as_str = f"The moon is { moon_aspect } to { trans_dict[trans] } in { trans }"
#             if moon_aspect == True:
#                 moon_str_list.append(moon_as_str)
#                 return moon_str_list
            

#     moon_asp = get_moon_aspects()
#     sun_asp = get_sun_aspects()

def get_moon_phase(current_date):
    xmoon_dict = web_scrape.moon_dict
    if current_date in xmoon_dict.keys():
        return xmoon_dict[current_date][0]

def get_solar_eclipse():
    """pull eclipse info from swe"""

    sol_ecl_data = swe.sol_eclipse_when_glob(converted_date)

    sol_ecl_time = swe.revjul(sol_ecl_data[1][0])

    return(sol_ecl_time)

def get_lunar_eclipse():
    """pull eclipse info from swe"""

    lun_ecl_data = swe.lun_eclipse_when(converted_date)

    lun_ecl_time = swe.revjul(lun_ecl_data[1][0])

    return(lun_ecl_time)


def get_retrogrades():
    """get current retrogrades in the sky"""


def create_user(email, password, phone_number):
    """Create and return a new user."""

    user = User(email=email, password=password, phone_number=phone_number)

    return user

def get_user_by_email(email):
    
    return User.query.filter(User.email == email).first()

def get_user_password(email, password):

    user = User.query.filter(User.email == email).first()   
    return user.password



if __name__ == '__main__':
    from server import app
    connect_to_db(app)