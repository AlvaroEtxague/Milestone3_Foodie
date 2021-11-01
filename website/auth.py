import os
from flask import (
    Blueprint,
    render_template,
    request,
    flash,
    redirect,
    url_for,
    session,
)
from mongo import CLUSTER, mongo_connect, DB, COLLECTION_USERS
from werkzeug.security import generate_password_hash, check_password_hash

if os.path.exists("env.py"):
    import env

auth = Blueprint("auth", __name__)

# mapping the db
db_connection = mongo_connect(CLUSTER)

# mapping the collection
users_collection = db_connection[DB][COLLECTION_USERS]
users = users_collection.find()


@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # get email and check if already exists in db
        email = request.form.get("email").lower()
        existing_user = users_collection.find_one({"email": email})

        # get the password entered
        password = request.form.get("password")

        # verify hashed password
        if existing_user:
            # if password is valid
            if check_password_hash(existing_user["password1"], password):
                username = existing_user["username"]
                session["user"] = username
                # flash("Welcome, {}".format(username))
                return redirect(
                    url_for("views.profile", username=session["user"])
                )
            else:
                # invalid password match
                flash(
                    "Incorrect username or password. " "Please try again.",
                    category="error",
                )
                return redirect(url_for("auth.login"))
        else:
            # username doesn't exist
            flash(
                "Incorrect username or password. Please try again.",
                category="error",
            )
            return redirect(url_for("auth.login"))
    return render_template("login.html")


@auth.route("/logout")
def logout():
    # remove user from session cookies
    flash("You have been logged out")
    session.pop("user")
    return redirect(url_for("auth.login"))


@auth.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form.get("email").lower()
        username = request.form.get("username").lower()
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")

        # validations
        existing_user = users_collection.find_one({"username": username})
        existing_email = users_collection.find_one({"email": email})

        # check if username already exists in db
        if existing_user:
            flash("Username already exists.", category="error")
            return redirect(url_for("auth.register"))

        # check if email already registered
        elif existing_email:
            flash(
                "This email is already registered. " "Please login.",
                category="error",
            )
            return redirect(url_for("auth.login"))

        elif len(email) < 4:
            # validate email
            flash("Please enter a valid email.", category="error")

        elif len(username) < 5 or len(username) > 20:
            # validate username
            flash(
                "Username must be between 5 and 20 characters.",
                category="error",
            )

        elif password1 != password2:
            # validate that passwords match
            flash("Passwords don't match.", category="error")

        elif len(password1) < 8:
            # validate password length
            flash(
                "Password must contain 8 or more characters.", category="error"
            )

        else:
            # add user to db
            # sending user info to db
            new_user = {
                "email": email,
                "username": username,
                "password1": generate_password_hash(password1),
                "password2": generate_password_hash(password2),
            }
            users_collection.insert_one(new_user)
            # success alert
            flash("Account created!", category="success")

            # redirect user to profile page
            return redirect(url_for("auth.login"))
    return render_template("register.html")
