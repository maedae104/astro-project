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

'''This is the server'''


@app.route('/')
def index():

    return render_template('homepage.html')


@app.route('/transits')
def get_transits():
    sun_long= crud.sun_ecl_long
    sun_sign = crud.calculate_sign(sun_long)
    moon_long = crud.moon_ecl_long
    moon_sign = crud.calculate_sign(moon_long)
    current_date = crud.current_date
    moon_phase = crud.get_moon_phase(current_date)

    return render_template('transits.html', sun_long=sun_long, sun_sign=sun_sign, moon_long=moon_long, moon_sign=moon_sign, current_date=current_date,  moon_phase=moon_phase)

@app.route("/", methods=["POST"])
def create_user():

    email = request.form.get("email")
    password = request.form.get("password")
    phone_number = request.form.get("phone_number")
    output = crud.check_user_email(email)
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
    
    user = crud.check_user_email(email)


    if user == None:
        flash("Please create an account.")
    else:
        if crud.get_user_password(email, password) == password:
            flash("You are logged in.")
            session["current_user"] = user.user_id
        else:
            flash("Those passwords don't match.")
    
    return redirect("/", user=user)

@app.route('/user-logout')
def logout():

    return render_template("hompage.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
