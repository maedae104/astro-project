from flask import (Flask, redirect, url_for, render_template, request,
                    flash, session)
import crud
import web_scrape
from model import connect_to_db, db, User, Transit, TextUpdates
from datetime import date

from jinja2 import StrictUndefined



app = Flask(__name__   )
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined

@app.route('/')
def index():

    return render_template('homepage.html')


@app.route('/transits')
def get_transits():

    current_date = crud.current_date
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

    transit = Transit(date=current_date, sun_sign = sun_sign, moon_sign = moon_sign, moon_phase=moon_phase, merc_sign = merc_sign, venus_sign = venus_sign, mars_sign=mars_sign, 
                             jup_sign = jup_sign, sat_sign = sat_sign, uran_sign = uran_sign, nept_sign = nept_sign,
                             pluto_sign = pluto_sign)
    db.session.add(transit)
    db.session.commit()

    return render_template('transits.html', sun_long=sun_long, sun_sign=sun_sign,
                             moon_long=moon_long, moon_sign=moon_sign, current_date=current_date, 
                             moon_phase=moon_phase, merc_long=merc_long, venus_long=venus_long,
                             mars_long = mars_long, jup_long=jup_long, sat_long=sat_long, 
                             uran_long = uran_long, nept_long = nept_long, pluto_long=pluto_long,
                             merc_sign = merc_sign, venus_sign = venus_sign, mars_sign=mars_sign, 
                             jup_sign = jup_sign, sat_sign = sat_sign, uran_sign = uran_sign, nept_sign = nept_sign,
                             pluto_sign = pluto_sign, transit = transit)

@app.route("/users", methods=["POST"])
def create_user():

    email = request.form.get("email")
    password = request.form.get("password")
    phone_number = request.form.get("phone_number")
    output = crud.get_user_by_email(email)
    new_user = User(email=email, password=password, phone_number=phone_number)

    if output != None:
        flash("OH NO, that users email already exists.")
    else:
        flash("Good job you created an account.")
        db.session.add(new_user)
        db.session.commit()

    return redirect("/")

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

@app.route('/user-logout')
def logout():
    ''' Logout user '''
    
    session.pop("user_email", None)

    return redirect("/")

if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)
    