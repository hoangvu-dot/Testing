from flask import Flask,flash, render_template, url_for, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///verification.sqlite3"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.permanent_session_lifetime = timedelta(minutes= 5)
app.secret_key = "Verification"

db = SQLAlchemy(app)

class users(db.Model):
    _id = db.Column("id", db.Integer, primary_key = True)
    name = db.Column(db.String(100))
    password = db.Column(db.String(100))

    def __init__(self, name, password):
        self.name = name
        self.password = password


@app.route("/view")
def view():
    return render_template("view.html", values = users.query.all())


@app.route("/register" , methods = ["POST", "GET"])
def register():
    if request.method == "POST":
        user = request.form["name"]
        password = request.form["pass"]

        found_user = users.query.filter_by(name = user).first()
        if found_user:
            flash(" ACCOUNT EXISTED, PLEASE LOG IN!")
            session.pop("user",None)
            session.pop("pass", None)
            return render_template("register.html")

        else:
            flash("REGISTER SUCCESFULLY, You can now log in")
            account = users(user, password)
            db.session.add(account)
            db.session.commit()
            return render_template("register.html")
    else:
        return render_template("register.html")

@app.route("/" , methods = ["POST", "GET"])
@app.route("/login" , methods = ["POST", "GET"])
def login():
    if request.method == "POST":
        user = request.form["name"]
        password = request.form["pass"]
    
        session.permanent = True
        session["user"] = user
        
        found_user = users.query.filter_by(name = user).first()

        if found_user:
            
            if password == found_user.password:
                return redirect(url_for("home"))
            else:
                flash("Please type the correct PASSWORD !")
                session.pop("user",None)
                session.pop("pass", None)
                return render_template("login.html")
        
        else:
            flash("You've not register yet")
            session.pop("user",None)
            session.pop("pass", None)
            return render_template("login.html")
        
    
    else:
        if "user" in session:
            flash("Already Logged in")
            return redirect(url_for("home"))
        
        return render_template("login.html")
    
@app.route("/home", methods = ["POST", "GET"])
def home():
    return render_template("home.html")

@app.route("/logout")
def logout():
    session.pop("user", None)
    session.pop("password",None)
    return redirect(url_for("login"))

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
