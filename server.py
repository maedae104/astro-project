from flask import Flask, redirect, url_for, render_template, request, flash


app = Flask(__name__   )

'''This is the server'''


@app.route('/')
def index():

    return render_template("hompage.html")


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



