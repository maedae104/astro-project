from flask import Flask, redirect, url_for, render_template, request, flash


app = Flask(__name__   )

'''This is the server'''


@app.route('/')
def index():

    return render_template('homepage.html')


@app.route('/transits')
def get_transits():

    sun_sign = "The sun is in Aries"
    moon_sign = "The moon is in Libra"
    moon_phase = "The moon is full"

    return render_template('transits.html', moon_sign=moon_sign, moon_phase=moon_phase, sun_sign=sun_sign)

@app.route("/users", methods=["POST"])
def create_user():

    email = request.form.get("email")
    password = request.form.get("password")
    output = crud.check_user_email(email)
    new_user = User(email=email, password=password)

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
    
    return redirect("/")

@app.route('/user-logout')
def logout():

    return render_template("hompage.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
