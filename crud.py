import json
import swisseph as swe
import web_scrape
from model import connect_to_db, db, User, Transit, TextUpdates
from datetime import date, datetime, timedelta
from flask_sqlalchemy import SQLAlchemy

swe.set_ephe_path('/usr/share/sweph/ephe')

today = date.today()
c_today = today.strftime("%Y %m %d")
c_today = c_today.split(' ')

year = int(c_today[0])
month = int(c_today[1])
day = int(c_today[2])

current_date = today.strftime("%b%-d")
converted_date = swe.julday(year, month, day)

yesterday = today - timedelta(days=1)

c_yday = yesterday.strftime("%Y %m %d")
c_yday = c_yday.split(' ')

y_day = int(c_yday[2])
y_year = int(c_yday[0])
y_month = int(c_yday[1])

y_converted = swe.julday(y_year, y_month, y_day)

tomorrow = today + timedelta(days=1)

c_tday = tomorrow.strftime("%Y %m %d")
c_tday = c_tday.split(' ')

t_day = int(c_yday[2])
t_year = int(c_yday[0])
t_month = int(c_yday[1])

t_converted = swe.julday(t_year, t_month, t_day)


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

y_sun_calcs = swe.calc_ut(y_converted, 0)
y_moon_calcs = swe.calc_ut(y_converted, 1)
y_merc_calcs = swe.calc_ut(y_converted, 2)
y_venus_calcs = swe.calc_ut(y_converted, 3)
y_mars_calcs = swe.calc_ut(y_converted, 4)
y_jup_calcs = swe.calc_ut(y_converted, 5)
y_sat_calcs = swe.calc_ut(y_converted, 6)
y_uran_calcs = swe.calc_ut(y_converted, 7)
y_nept_calcs = swe.calc_ut(y_converted, 8)
y_pluto_calcs = swe.calc_ut(y_converted, 9)

y_sun_ecl_long = y_sun_calcs[0][0]
y_moon_ecl_long = y_moon_calcs[0][0]
y_merc_ecl_long = y_merc_calcs[0][0]
y_venus_ecl_long = y_venus_calcs[0][0]
y_mars_ecl_long = y_mars_calcs[0][0]
y_jup_ecl_long = y_jup_calcs[0][0]
y_sat_ecl_long = y_sat_calcs[0][0]
y_uran_ecl_long = y_uran_calcs[0][0]
y_nept_ecl_long = y_nept_calcs[0][0]
y_pluto_ecl_long = y_pluto_calcs[0][0]


t_sun_calcs = swe.calc_ut(t_converted, 0)
t_moon_calcs = swe.calc_ut(t_converted, 1)
t_merc_calcs = swe.calc_ut(t_converted, 2)
t_venus_calcs = swe.calc_ut(t_converted, 3)
t_mars_calcs = swe.calc_ut(t_converted, 4)
t_jup_calcs = swe.calc_ut(t_converted, 5)
t_sat_calcs = swe.calc_ut(t_converted, 6)
t_uran_calcs = swe.calc_ut(t_converted, 7)
t_nept_calcs = swe.calc_ut(t_converted, 8)
t_pluto_calcs = swe.calc_ut(t_converted, 9)

t_sun_ecl_long = t_sun_calcs[0][0]
t_moon_ecl_long = t_moon_calcs[0][0]
t_merc_ecl_long = t_merc_calcs[0][0]
t_venus_ecl_long = t_venus_calcs[0][0]
t_mars_ecl_long = t_mars_calcs[0][0]
t_jup_ecl_long = t_jup_calcs[0][0]
t_sat_ecl_long = t_sat_calcs[0][0]
t_uran_ecl_long = t_uran_calcs[0][0]
t_nept_ecl_long = t_nept_calcs[0][0]
t_pluto_ecl_long = t_pluto_calcs[0][0]

def calculate_sign(ecl_long):
    """Calculate the planet's current sign based on degrees"""
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
        return "Conjunct"

    elif sign_dict[planet_b] == sign_dict[planet_a] + 2 or sign_dict[planet_b] == sign_dict[planet_a] + 10:
        return "Sextile"

    elif sign_dict[planet_a] == sign_dict[planet_b] + 2 or sign_dict[planet_a] == sign_dict[planet_b] + 10:
        return "Sextile"

    elif sign_dict[planet_b] == sign_dict[planet_a] + 3 or sign_dict[planet_b] == sign_dict[planet_a] + 9:
        return "Square"

    elif sign_dict[planet_a] == sign_dict[planet_b] + 3 or sign_dict[planet_a] == sign_dict[planet_b] + 9:
        return "Square"
    
    elif sign_dict[planet_b] == sign_dict[planet_a] + 4 or sign_dict[planet_b] == sign_dict[planet_a] + 8:
        return "Trine"

    elif sign_dict[planet_a] == sign_dict[planet_b] + 4 or sign_dict[planet_a] == sign_dict[planet_b] + 8:
        return "Trine"

    elif sign_dict[planet_b] == sign_dict[planet_a] + 6:
        return "Opposition"

    elif sign_dict[planet_a] == sign_dict[planet_b] + 6:
        return "Opposition"
            
sun_sign = calculate_sign(sun_ecl_long)
moon_sign = calculate_sign(moon_ecl_long)
merc_sign = calculate_sign(merc_ecl_long)
venus_sign = calculate_sign(venus_ecl_long)
mars_sign = calculate_sign(mars_ecl_long)
jup_sign = calculate_sign(jup_ecl_long)
sat_sign = calculate_sign(sat_ecl_long)
uran_sign = calculate_sign(uran_ecl_long)
nept_sign = calculate_sign(nept_ecl_long)
pluto_sign = calculate_sign(pluto_ecl_long)

transit_list = [sun_sign, moon_sign, merc_sign, venus_sign, mars_sign, jup_sign, sat_sign, uran_sign, nept_sign, pluto_sign]

trans_dict = {
        "the Sun" : sun_sign ,
        "the Moon" : moon_sign , 
        "Mercury" : merc_sign ,
        "Venus" : venus_sign  ,
        "Mars" : mars_sign  ,
        "Jupiter" : jup_sign ,
        "Saturn" : sat_sign ,
        "Neptune" : nept_sign , 
        "Pluto" : pluto_sign }
    
y_sun_sign = calculate_sign(y_sun_ecl_long)
y_moon_sign = calculate_sign(y_moon_ecl_long)
y_merc_sign = calculate_sign(y_merc_ecl_long)
y_venus_sign = calculate_sign(y_venus_ecl_long)
y_mars_sign = calculate_sign(y_mars_ecl_long)
y_jup_sign = calculate_sign(y_jup_ecl_long)
y_sat_sign = calculate_sign(y_sat_ecl_long)
y_uran_sign = calculate_sign(y_uran_ecl_long)
y_nept_sign = calculate_sign(y_nept_ecl_long)
y_pluto_sign = calculate_sign(y_pluto_ecl_long)

y_transit_list = [y_sun_sign, y_moon_sign, y_merc_sign, y_venus_sign,
y_mars_sign, y_jup_sign, y_sat_sign, y_uran_sign, y_nept_sign, y_pluto_sign]

y_trans_dict = {
        "the Sun" : y_sun_sign ,
        "the Moon" : y_moon_sign , 
        "Mercury" : y_merc_sign ,
        "Venus" : y_venus_sign  ,
        "Mars" : y_mars_sign  ,
        "Jupiter" : y_jup_sign ,
        "Saturn" : y_sat_sign ,
        "Neptune" : y_nept_sign , 
        "Pluto" : y_pluto_sign }

t_sun_sign = calculate_sign(t_sun_ecl_long)
t_moon_sign = calculate_sign(t_moon_ecl_long)
t_merc_sign = calculate_sign(t_merc_ecl_long)
t_venus_sign = calculate_sign(t_venus_ecl_long)
t_mars_sign = calculate_sign(t_mars_ecl_long)
t_jup_sign = calculate_sign(t_jup_ecl_long)
t_sat_sign = calculate_sign(t_sat_ecl_long)
t_uran_sign = calculate_sign(t_uran_ecl_long)
t_nept_sign = calculate_sign(t_nept_ecl_long)
t_pluto_sign = calculate_sign(t_pluto_ecl_long)

t_transit_list = [t_sun_sign, t_moon_sign, t_merc_sign, t_venus_sign,
t_mars_sign, t_jup_sign, t_sat_sign, t_uran_sign, t_nept_sign, t_pluto_sign]

t_trans_dict = {
        "the Sun" : t_sun_sign ,
        "the Moon" : t_moon_sign , 
        "Mercury" : t_merc_sign ,
        "Venus" : t_venus_sign  ,
        "Mars" : t_mars_sign  ,
        "Jupiter" : t_jup_sign ,
        "Saturn" : t_sat_sign ,
        "Neptune" : t_nept_sign , 
        "Pluto" : t_pluto_sign }

def get_sun_aspects():
    """Calculate aspects to the sun"""
    
    sun_aspect_list = []
    planets = trans_dict.keys()

    for planet in planets:
        sun_aspect = get_aspects(trans_dict[planet], transit_list[0])
        sun_as_str = f"{ sun_aspect } to { planet } in { trans_dict[planet] }"
        
        if planet == "the Sun":
            pass

        elif sun_aspect != None:
             sun_aspect_list.append(sun_as_str)
    
    return sun_aspect_list 

def y_get_sun_aspects():
    """Calculate aspects to the sun"""
    
    sun_aspect_list = []
    planets = y_trans_dict.keys()

    for planet in planets:
        y_sun_aspect = get_aspects(y_trans_dict[planet], transit_list[0])
        sun_as_str = f"{ y_sun_aspect } to { planet } in { y_trans_dict[planet] }"
        
        if planet == "the Sun":
            pass

        elif y_sun_aspect != None:
             sun_aspect_list.append(sun_as_str)
    
    return sun_aspect_list 

def t_get_sun_aspects():
    """Calculate aspects to the sun"""
    
    sun_aspect_list = []
    planets = t_trans_dict.keys()

    for planet in planets:
        t_sun_aspect = get_aspects(t_trans_dict[planet], transit_list[0])
        sun_as_str = f"{ t_sun_aspect } to { planet } in { t_trans_dict[planet] }"
        
        if planet == "the Sun":
            pass

        elif t_sun_aspect != None:
             sun_aspect_list.append(sun_as_str)
    
    return sun_aspect_list 

def get_moon_aspects():
    """Calculate aspects to the moon"""

    moon_aspect_list = []
    planets = trans_dict.keys()

    for planet in planets:
        moon_aspect = get_aspects(trans_dict[planet], transit_list[1])
        
        moon_as_str = f"{ moon_aspect } to { planet } in { trans_dict[planet] }"

        if planet == "the Moon":
            pass

        elif moon_aspect != None:
            moon_aspect_list.append(moon_as_str)
        
    return moon_aspect_list

def y_get_moon_aspects():
    """Calculate aspects to the moon"""

    moon_aspect_list = []
    planets = y_trans_dict.keys()

    for planet in planets:
        y_moon_aspect = get_aspects(y_trans_dict[planet], y_transit_list[1])
        
        moon_as_str = f"{ y_moon_aspect } to { planet } in { y_trans_dict[planet] }"

        if planet == "the Moon":
            pass

        elif y_moon_aspect != None:
            moon_aspect_list.append(moon_as_str)
        
    return moon_aspect_list

def t_get_moon_aspects():
    """Calculate aspects to the moon"""

    moon_aspect_list = []
    planets = t_trans_dict.keys()

    for planet in planets:
        t_moon_aspect = get_aspects(t_trans_dict[planet], t_transit_list[1])
        
        moon_as_str = f"{ t_moon_aspect } to { planet } in { t_trans_dict[planet] }"

        if planet == "the Moon":
            pass

        elif t_moon_aspect != None:
            moon_aspect_list.append(moon_as_str)
        
    return moon_aspect_list

def get_moon_phase(current_date):
    """Get current moon phase"""

    xmoon_dict = web_scrape.moon_dict
    if current_date in xmoon_dict.keys():
        return xmoon_dict[current_date][0]

def get_retro(current_date):
    """get current retrogrades in the sky"""

    xretro_dict = web_scrape.retro_dict

    xretro_dates = xretro_dict.keys()

   
    current_date = today.strftime("%m%-d")
    i=0
    
    while len(xretro_dates) - 1:
        for r_date in xretro_dates:
            if int(current_date) >= int(r_date):
                return xretro_dict[r_date]

def is_retro(retro_data):


    retro_data = get_retro(current_date)

    if "Pre-shadow Begins" in retro_data:
        return "Mercury is in its pre-shadow"

    if "Retrograde Begins" in retro_data:
        return "Mercury is currently retrograde"

    if "Post-Shadow Begins" in retro_data:
        return "Mercury is in its post-shadow"

    if "Post-Shadow Ends" in retro_data:
        return "Mercury is stationed direct"


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