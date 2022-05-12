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


@app.route("/create-user")
def display_create_user():

    return render_template("createuser.html")

@app.route("/users", methods=["POST"])
def create_user():

    email = request.form.get("email")
    password = request.form.get("password")
    phone_number = request.form.get("phone")
    output = crud.get_user_by_email(email)
    new_user = User(email=email, password=password, phone_number=phone_number)

    if output != None:
        flash("OH NO, that users email already exists.")                        
    else:
        flash("Good job you created an account.")
        db.session.add(new_user)
        db.session.commit()

    return redirect("/")

@app.route("/login")
def display_login():

    return render_template("userlogin.html")

@app.route("/login", methods=["POST"])
def user_login():

    email = request.form.get("email")
    password = request.form.get("password")
    phone_number = request.form.get("phone_number")

    user = crud.get_user_by_email(email)
    session['phone_number'] = user.phone_number

    if not user or user.password != password:
        flash("The email or password you entered was incorrect.")
    else:
        session["user_email"] = user.email
        flash(f"Welcome back, {user.email}!")

    return render_template('userProfile.html')

@app.route("/updates")
def send_user_updates():

    transit_update = Transit.query.filter_by(date = crud.current_date)
    email = request.form.get("email")
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

    text_update = TextUpdates(transit_date = date, user_id = user.user_id)
    db.session.add(text_update)
    db.session.commit()

    return render_template('userProfile.html')  

# @app.route('/user-profile')
# def display_profile():
    
#     if not session['user_email']:
#         flash("OH NO, please login to see your profile")
#         return redirect('/login')

#     else:
#         return render_template('userProfile.html')

@app.route('/user-logout')
def logout():
    ''' Logout user '''
    
    session.pop("user_email", None)

    return redirect("/")

if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)
    