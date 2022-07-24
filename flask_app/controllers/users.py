from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models import user, post
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route("/")
def index():
    return render_template("index.html")

@app.route('/register',methods=['POST'])
def register():
    if not user.User.validate_user(request.form):
        return redirect('/')
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    print(pw_hash)
    data = {
        "username" : request.form['username'],
        "email" : request.form['email'],
        "password" : pw_hash
        }
    id = user.User.save(data)
    session["user_id"] = id
    return redirect('/dashboard')


@app.route('/login', methods=["POST"])
def login():
    login_user = user.User.get_by_email(request.form)
    if not login_user:
        flash("Username not recognized", "login")
        return redirect("/")
    if not bcrypt.check_password_hash(login_user.password, request.form["password"]):
        flash("Password not recognized", "login")
        return redirect("/")
    session["user_id"] = login_user.id
    return redirect("/dashboard")


@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect("logout")
    data ={
        "id": session["user_id"]
    }
    return render_template("dashboard.html", user=user.User.get_by_id(data), posts=post.Post.get_all_with_likes())

