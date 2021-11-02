from flask import (
    Blueprint,
    render_template,
    request,
    flash,
    redirect,
    url_for,
    session,
    jsonify,
)
from bson.objectid import ObjectId
from mongo import (
    CLUSTER,
    mongo_connect,
    DB,
    COLLECTION_POSTS,
    COLLECTION_USERS,
    COLLECTION_RATINGS,
    COLLECTION_FAVOURITE,
)

views = Blueprint("views", __name__)

db_connection = mongo_connect(CLUSTER)
posts_collection = db_connection[DB][COLLECTION_POSTS]
users_collection = db_connection[DB][COLLECTION_USERS]
ratings_collection = db_connection[DB][COLLECTION_RATINGS]
favourite_collection = db_connection[DB][COLLECTION_FAVOURITE]


# HOME VIEW
@views.route("/")
def home():
    posts = posts_collection.find()
    try:
        creator = session["user"]
    except:
        creator = "None"
    return render_template("home.html", posts=posts, creator=creator)


# INDIVIDUAL POST VIEW
@views.route("/post/<username>/<post_id>", methods=["GET", "POST"])
def post(post_id, username):
    try:
        creator = session["user"]
        username = users_collection.find_one({"username": session["user"]})[
            "username"
        ]
        post = posts_collection.find_one({"_id": ObjectId(post_id)})
        ratings = ratings_collection.find()
        can_create = "yes"
        rating = 0
        if session["user"]:
            for data in ratings:
                if data["user_id"] == username and data["post_id"] == post_id:
                    can_create = "no"
                    rating = data["rate"]
                    break

            print(rating)
            print(can_create)
            return render_template(
                "post.html",
                post=post,
                can_create=can_create,
                rating=int(rating),
                creator=creator,
            )
    except:
        creator = "None"
        post = posts_collection.find_one({"_id": ObjectId(post_id)})
        ratings = ratings_collection.find()
        can_create = "yes"
        rating = 0
        return render_template(
            "post.html",
            post=post,
            can_create=can_create,
            rating=int(rating),
            creator=creator,
        )


# ADD FAVORITE RECIPES
@views.route("/favourite/<post_id>", methods=["GET", "POST"])
def favourite(post_id):
    try:
        creator = session["user"]

        to_check = favourite_collection.find_one({"post_id": post_id})
        post = posts_collection.find_one({"_id": ObjectId(post_id)})
        if to_check:
            print("Already present")
            return redirect("/")
        else:
            new_post = {
                "post_id": post_id,
                "post_title": post["post_title"],
                "post_description": post["post_description"],
                "user_id": post["user_id"],
                "image_url": post["image_url"],
                "prep_time": post["prep_time"],
                "rating": post["rating"],
                "saved_by": creator,
            }
            favourite_collection.insert_one(new_post)
            # success alert
            flash("Added to favourites.", category="success")

            return redirect("/")
    except:
        return redirect(url_for("auth.login"))


# ADD RATING FOR POST
@views.route("/rating/<post_id>", methods=["GET", "POST"])
def rating(post_id):
    try:
        creator = session["user"]
        if request.method == "POST":
            rate = request.form["rate"]
            post = posts_collection.find_one({"_id": ObjectId(post_id)})

            rating_data = {"rate": rate, "user_id": creator, "post_id": post_id}

            ratings_collection.insert_one(rating_data)
            ratings = ratings_collection.find({"post_id": post_id})
            rate_list = []

            for data in ratings:
                rate_list.append(data["rate"])
                print(data["user_id"])

            one_star = 0
            two_star = 0
            three_star = 0
            four_star = 0
            five_star = 0
            total_number_of_rating = 0

            for number in rate_list:
                print(number)
                if int(number) == 1:
                    one_star = one_star + 1
                elif int(number) == 2:
                    two_star = two_star + 1
                elif int(number) == 3:
                    three_star = three_star + 1
                elif int(number) == 4:
                    four_star = four_star + 1
                else:
                    five_star = five_star + 1

                total_number_of_rating = total_number_of_rating + 1

            final_rating = (
                1 * int(one_star)
                + 2 * int(two_star)
                + 3 * int(three_star)
                + 4 * int(four_star)
                + 5 * int(five_star)
            ) / int(total_number_of_rating)

            updated_post = {
                "post_title": post["post_title"],
                "post_description": post["post_description"],
                "user_id": post["user_id"],
                "image_url": post["image_url"],
                "prep_time": post["prep_time"],
                "rating": final_rating,
            }

            posts_collection.update({"_id": ObjectId(post_id)}, updated_post)
            return redirect(
                url_for("views.post", post_id=post_id, username=creator)
            )
    except:
        try:
            creator = session["user"]
            post = posts_collection.find_one({"_id": ObjectId(post_id)})
            print("logged user no rating")
            flash(
                "Please select a rating",
                category="error",
            )
            return redirect(
                url_for("views.post", post_id=post_id, username=creator)
            )
        except:
            print("not logged user")
            flash(
                "Please login to select a rating",
                category="error",
            )
            return redirect(url_for("auth.login"))


# USER PROFILE VIEW
@views.route("/profile/<username>", methods=["GET", "POST"])
def profile(username):
    creator = session["user"]
    username = users_collection.find_one({"username": session["user"]})[
        "username"
    ]

    posts = posts_collection.find({"user_id": username})

    fav = favourite_collection.find()
    if session["user"]:
        if posts.count() > 0:
            return render_template(
                "profile.html",
                username=username,
                posts=posts,
                creator=creator,
                fav=fav,
            )
        else:
            flash(
                "You don't have any recipes yet. Let's create one!",
                category="success",
            )
            return render_template(
                "profile.html",
                username=username,
                posts=posts,
                creator=creator,
                fav=fav,
            )
    return redirect(url_for("login"))


# ADD NEW POST VIEW
@views.route("/add_post", methods=["GET", "POST"])
def add_post():
    if request.method == "POST":
        creator = session["user"]
        post_title = request.form.get("post-title")
        post_description = request.form.get("description")
        image_url = request.form.get("image-url")
        prep_time = request.form.get("prep-time")

        # send new post details to DB
        new_post = {
            "post_title": post_title,
            "post_description": post_description,
            "user_id": creator,
            "image_url": image_url,
            "prep_time": prep_time,
            "rating": 0,
        }
        posts_collection.insert_one(new_post)

        # success alert
        flash("New post created!", category="success")
        return redirect(url_for("views.profile", username=creator))
    return render_template("add_post.html")


# UPDATE POST VIEW
@views.route("/edit_post/<post_id>", methods=["GET", "POST"])
def edit_post(post_id):
    if request.method == "POST":
        creator = session["user"]
        post_title = request.form.get("post-title")
        post_description = request.form.get("description")
        image_url = request.form.get("image-url")
        prep_time = request.form.get("prep-time")
        rating = request.form.get("rating")
        updated_post = {
            "post_title": post_title,
            "post_description": post_description,
            "user_id": creator,
            "image_url": image_url,
            "prep_time": prep_time,
            "rating": float(rating),
        }

        posts_collection.update({"_id": ObjectId(post_id)}, updated_post)
        flash("Your post has been updated.", category="success")
        return redirect(url_for("views.profile", username=creator))
    post = posts_collection.find_one({"_id": ObjectId(post_id)})
    return render_template("update_post.html", post=post)


# DELETE POST VIEW
@views.route("/delete_post/<post_id>")
def delete_post(post_id):
    creator = session["user"]
    posts_collection.delete_one({"_id": ObjectId(post_id)})
    flash("Your post has been deleted.", category="success")

    return redirect(url_for("views.profile", username=creator))


# DELETE POST VIEW
@views.route("/delete_fav_post/<post_id>")
def delete_fav_post(post_id):
    creator = session["user"]
    favourite_collection.delete_one({"_id": ObjectId(post_id)})
    flash("Removed from favourites", category="success")

    return redirect(url_for("views.profile", username=creator))


# SEARCH BAR VIEW
@views.route("/search", methods=["GET", "POST"])
def search():
    query = request.form.get("query")
    posts = posts_collection.find({"$text": {"$search": query}})
    if posts.count() > 0:
        return render_template("home.html", posts=posts)
    else:
        flash("No recipes found. Please try again.", category="error")
        return render_template("home.html", posts=posts)
