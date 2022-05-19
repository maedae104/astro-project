from flask import (Flask, redirect, url_for, render_template, request,
                    flash, session, jsonify)
import crud
import web_scrape
from model import connect_to_db, db, User, Transit, TextUpdates
from datetime import date
from jinja2 import StrictUndefined
import os
from twilio.rest import Client
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__   )
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined

@app.route('/')
def index():

    return render_template('homepage.html')


@app.route('/transits')
def get_transits():

    current_date = crud.current_date
    today = crud.today
    moon_phase = crud.get_moon_phase(current_date)
    
    sun_long= crud.sun_ecl_long
    sun_sign = crud.calculate_sign(sun_long)

    moon_long = crud.moon_ecl_long
    moon_sign = crud.calculate_sign(moon_long)

    merc_long = crud.merc_ecl_long
    merc_sign = crud.calculate_sign(merc_long)

    venus_long = crud.venus_ecl_long
    venus_sign = crud.calculate_sign(venus_long)

    mars_long = crud.mars_ecl_long
    mars_sign = crud.calculate_sign(mars_long)

    jup_long = crud.jup_ecl_long
    jup_sign = crud.calculate_sign(jup_long)

    sat_long = crud.sat_ecl_long
    sat_sign = crud.calculate_sign(sat_long)

    uran_long = crud.uran_ecl_long
    uran_sign = crud.calculate_sign(uran_long)

    nept_long = crud.nept_ecl_long
    nept_sign = crud.calculate_sign(nept_long)

    pluto_long = crud.pluto_ecl_long
    pluto_sign = crud.calculate_sign(pluto_long)

    solar_ecl = crud.get_solar_eclipse()

    sun_day = solar_ecl[2]
    sun_month = solar_ecl[1]
    sun_year = solar_ecl[0]

    lunar_ecl = crud.get_lunar_eclipse()

    moon_day = lunar_ecl[2]
    moon_month = lunar_ecl[1]
    moon_year = lunar_ecl[0]

    transit = Transit(date=current_date, sun_sign = sun_sign, moon_sign = moon_sign, moon_phase=moon_phase, merc_sign = merc_sign, venus_sign = venus_sign, mars_sign=mars_sign, 
                             jup_sign = jup_sign, sat_sign = sat_sign, uran_sign = uran_sign, nept_sign = nept_sign,
                             pluto_sign = pluto_sign)
    db.session.add(transit)
    db.session.commit()
    
    moon_aspects = crud.get_moon_aspects()
    sun_aspects = crud.get_sun_aspects()
    
    merc_retro = crud.is_retro(crud.get_retro(current_date))

    return render_template('transits.html', sun_long=sun_long, sun_sign=sun_sign,
                             moon_long=moon_long, moon_sign=moon_sign, current_date=current_date, 
                             moon_phase=moon_phase, merc_long=merc_long, venus_long=venus_long,
                             mars_long = mars_long, jup_long=jup_long, sat_long=sat_long, 
                             uran_long = uran_long, nept_long = nept_long, pluto_long=pluto_long,
                             merc_sign = merc_sign, venus_sign = venus_sign, mars_sign=mars_sign, 
                             jup_sign = jup_sign, sat_sign = sat_sign, uran_sign = uran_sign, nept_sign = nept_sign,
                             pluto_sign = pluto_sign, transit = transit, solar_ecl=solar_ecl, sun_day=sun_day,
                             sun_year=sun_year, sun_month=sun_month, lunar_ecl=lunar_ecl, moon_day = moon_day,
                             moon_month=moon_month, moon_year=moon_year, today=today, moon_aspects= moon_aspects, sun_aspects=sun_aspects, merc_retro = merc_retro)

@app.route('/yesterday-transits')
def yesterday_transits():
    """Returns yesterdays transits"""

    yesterday = crud.yesterday
    current_yday = yesterday.strftime("%b%-d")

    y_moon_phase = crud.get_moon_phase(current_yday)
    
    y_sun_long= crud.y_sun_ecl_long
    y_sun_sign = crud.calculate_sign(y_sun_long)

    y_moon_long = crud.y_moon_ecl_long
    y_moon_sign = crud.calculate_sign(y_moon_long)

    y_merc_long = crud.y_merc_ecl_long
    y_merc_sign = crud.calculate_sign(y_merc_long)

    y_venus_long = crud.y_venus_ecl_long
    y_venus_sign = crud.calculate_sign(y_venus_long)

    y_mars_long = crud.y_mars_ecl_long
    y_mars_sign = crud.calculate_sign(y_mars_long)

    y_jup_long = crud.y_jup_ecl_long
    y_jup_sign = crud.calculate_sign(y_jup_long)

    y_sat_long = crud.y_sat_ecl_long
    y_sat_sign = crud.calculate_sign(y_sat_long)

    y_uran_long = crud.y_uran_ecl_long
    y_uran_sign = crud.calculate_sign(y_uran_long)

    y_nept_long = crud.y_nept_ecl_long
    y_nept_sign = crud.calculate_sign(y_nept_long)

    y_pluto_long = crud.y_pluto_ecl_long
    y_pluto_sign = crud.calculate_sign(y_pluto_long)

    solar_ecl = crud.get_solar_eclipse()
    lunar_ecl = crud.get_lunar_eclipse()

    merc_retro = crud.is_retro(crud.get_retro(crud.y_converted))

    y_moon_aspects = crud.y_get_moon_aspects()

    moon_day = lunar_ecl[2]
    moon_month = lunar_ecl[1]
    moon_year = lunar_ecl[0]

    y_sun_aspects = crud.y_get_sun_aspects()

    sun_day = solar_ecl[2]
    sun_month = solar_ecl[1]
    sun_year = solar_ecl[0]
   

    return render_template("yesterdays-transits.html",  y_sun_sign= y_sun_sign,  y_moon_sign =  y_moon_sign,  y_moon_phase= y_moon_phase,
                              y_merc_sign =  y_merc_sign,  y_venus_sign =  y_venus_sign,  y_mars_sign=  y_mars_sign, 
                              y_jup_sign =  y_jup_sign,  y_sat_sign =  y_sat_sign,  y_uran_sign =  y_uran_sign,  y_nept_sign =  y_nept_sign,
                              y_pluto_sign =  y_pluto_sign, current_yday = current_yday, solar_ecl=solar_ecl, lunar_ecl=lunar_ecl, merc_retro=merc_retro, 
                              y_moon_aspects = y_moon_aspects, y_sun_aspects = y_sun_aspects, moon_day=moon_day, moon_month=moon_month, moon_year=moon_year, 
                              sun_day = sun_day, sun_month = sun_month, sun_year = sun_year)


@app.route('/tomorrow-transits')
def tommorrow_transits():
    """Returns tomorrows transits"""

    tomorrow = crud.tomorrow
    current_tday = tomorrow.strftime("%b%-d")

    t_moon_phase = crud.get_moon_phase(current_tday)
    
    t_sun_long= crud.t_sun_ecl_long
    t_sun_sign = crud.calculate_sign(t_sun_long)

    t_moon_long = crud.t_moon_ecl_long
    t_moon_sign = crud.calculate_sign(t_moon_long)

    t_merc_long = crud.t_merc_ecl_long
    t_merc_sign = crud.calculate_sign(t_merc_long)

    t_venus_long = crud.t_venus_ecl_long
    t_venus_sign = crud.calculate_sign(t_venus_long)

    t_mars_long = crud.t_mars_ecl_long
    t_mars_sign = crud.calculate_sign(t_mars_long)

    t_jup_long = crud.t_jup_ecl_long
    t_jup_sign = crud.calculate_sign(t_jup_long)

    t_sat_long = crud.t_sat_ecl_long
    t_sat_sign = crud.calculate_sign(t_sat_long)

    t_uran_long = crud.t_uran_ecl_long
    t_uran_sign = crud.calculate_sign(t_uran_long)

    t_nept_long = crud.t_nept_ecl_long
    t_nept_sign = crud.calculate_sign(t_nept_long)

    t_pluto_long = crud.t_pluto_ecl_long
    t_pluto_sign = crud.calculate_sign(t_pluto_long)

    solar_ecl = crud.get_solar_eclipse()
    lunar_ecl = crud.get_lunar_eclipse()

    merc_retro = crud.is_retro(crud.get_retro(crud.t_converted))

    t_moon_aspects = crud.t_get_moon_aspects()
    t_sun_aspects = crud.t_get_sun_aspects()


    sun_day = solar_ecl[2]
    sun_month = solar_ecl[1]
    sun_year = solar_ecl[0]

    moon_day = lunar_ecl[2]
    moon_month = lunar_ecl[1]
    moon_year = lunar_ecl[0]

    return render_template("tomorrows-transits.html",  t_sun_sign= t_sun_sign,  t_moon_sign =  t_moon_sign,  t_moon_phase= t_moon_phase,
                              t_merc_sign =  t_merc_sign,  t_venus_sign =  t_venus_sign,  t_mars_sign=  t_mars_sign, 
                              t_jup_sign =  t_jup_sign,  t_sat_sign =  t_sat_sign,  t_uran_sign =  t_uran_sign,  t_nept_sign =  t_nept_sign,
                              t_pluto_sign =  t_pluto_sign, current_tday=current_tday, solar_ecl=solar_ecl, 
                              lunar_ecl=lunar_ecl, merc_retro=merc_retro,t_moon_aspects=t_moon_aspects, t_sun_aspects=t_sun_aspects,
                              sun_day=sun_day, sun_month=sun_month, sun_year=sun_year, moon_day=moon_day, 
                              moon_month = moon_month, moon_year=moon_year)

@app.route("/create-user")
def display_create_user():

    return render_template("createuser.html")

@app.route("/users", methods=["POST"])
def create_user():

    email = request.form.get("email")
    password = request.form.get("password")
    phone_number = request.form.get("phone")
    output = crud.get_user_by_email(email)
    

    if output != None:
        flash("OH NO, that users email already exists.")                        
    else:
        flash("Good job you created an account.")
        new_user = User(email=email, password=password, phone_number=phone_number)
        db.session.add(new_user)
        db.session.commit()
        print("Reached here, check db")
        print("check new user again: ", new_user)

    return render_template("createuser.html")

@app.route("/login")
def display_login():

    return render_template("userlogin.html")

@app.route("/login", methods=["POST"])
def user_login():

    email = request.form.get("email")
    password = request.form.get("password")
   


    user = crud.get_user_by_email(email)
    

    if not user or user.password != password:
        flash("The email or password you entered was incorrect.")
        return redirect('/login')
    else:
        session["user_email"] = user.email
        session["phone_number"] = user.phone_number
        flash(f"Welcome back, {user.email}!") 
        return render_template('userprofile.html')


@app.route("/updates")
def send_user_updates():

    transit_update = Transit.query.filter_by(date = crud.current_date).first()
    print("transit update: ", transit_update)
    email = session['user_email']
    print("email: ", email)
    user = crud.get_user_by_email(email)
    
    account_sid = "AC991a3de185a36e54239a02cf95ce35de"
    auth_token  = os.environ['TWILIO_TOKEN']

    client = Client(account_sid, auth_token)

    message = client.messages.create(
    body= transit_update,
    from_='+19893680543',
    to= session['phone_number']
    )
    print(message)


    text_update = TextUpdates(transit_date = date.today(), user_id = user.user_id, transit_id = transit_update.transit_id)
    db.session.add(text_update)
    db.session.commit()

    return render_template('userProfile.html')  

@app.route('/user-profile')
def display_profile():
    
    
    return render_template('userProfile.html')

@app.route('/logout')
def logout():
    """ Logout user """
    
    session.pop("user_email", None)

    return redirect("/")

if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)
    