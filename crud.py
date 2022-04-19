import json
import swisseph as swe


def get_sun_sign():
    pass 

def get_moon_sign():
    pass
def get_moon_phase():
    pass

def create_user(email, password):
    """Create and return a new user."""

    user = User(email=email, password=password)

    return user

def check_user_email(x_email):
    
    return User.query.filter(User.email == x_email).first()

def get_user_password(x_email, x_password):

    x_user = User.query.filter(User.email == x_email).first()   
    return x_user.password



swe.set_ephe_path('/usr/share/sweph/ephe')

converted_date = swe.julday(2022, 4, 19)

res = swe.lun_eclipse_when(converted_date)

retflags = swe.calc_ut(converted_date, 0)

ecltime = swe.revjul(res[1][0])

sun = swe.get_planet_name(0)
moon = swe.get_planet_name(1)
swe.set_topo(8.58, 47.33, 473)

# 3.   Compute a planet or other bodies:

# ret_flag = swe_calc_ut(jul_day_UT, planet_no, flag, lon_lat_rad, err_msg);

# or a fixed star:

# ret_flag = swe_fixstar_ut(star_nam, jul_day_UT, flag, lon_lat_rad, err_msg);


