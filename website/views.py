from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from bson.objectid import ObjectId
from mongo import CLUSTER, mongo_connect, DB, COLLECTION_POSTS,COLLECTION_USERS

views = Blueprint('views', __name__)

db_connection = mongo_connect(CLUSTER)
posts_collection = db_connection[DB][COLLECTION_POSTS]
users_collection = db_connection[DB][COLLECTION_USERS]

# HOME VIEW
@views.route('/')
def home():
    posts = posts_collection.find()    
    return render_template("home.html", posts=posts)

# INDIVIDUAL POST VIEW
@views.route('/post/<username>/<post_id>', methods=['GET', 'POST'])
def post(post_id, username):
    post = posts_collection.find_one({"_id": ObjectId(post_id)})
    return render_template("post.html", post = post)

# USER PROFILE VIEW
@views.route('/profile/<username>', methods=['GET', 'POST'])
def profile(username):
    username = users_collection.find_one({"username": session["user"]})["username"]
    posts = posts_collection.find({"user_id": username})   

    if session["user"]:
        if posts.count() > 0 :
            return render_template("profile.html", username=username, posts=posts)
        else:
            flash("You don't have any recipes yet. Let's create one!", category='success')
            return render_template("profile.html", username=username, posts=posts)
    
    return redirect(url_for("login"))

# ADD NEW POST VIEW
@views.route('/add_post', methods=['GET', 'POST'])
def add_post():    
    if request.method == 'POST':
        creator = session["user"]
        post_title = request.form.get('post-title')
        post_description = request.form.get('description')
        image_url = request.form.get('image-url')
        prep_time = request.form.get('prep-time')
        
        # send new post details to DB
        new_post = {
            "post_title": post_title,
            "post_description": post_description,
            "user_id": creator,
            "image_url": image_url,
            "prep_time": prep_time,
        }
        posts_collection.insert_one(new_post)
        
        # success alert
        flash("New post created!", category='success')
        return redirect(url_for("views.profile", username=creator))
        
    return render_template("add_post.html")

# UPDATE POST VIEW
@views.route('/edit_post/<post_id>', methods=['GET', 'POST'])
def edit_post(post_id):    
    if request.method == 'POST':
        creator = session["user"]
        post_title = request.form.get('post-title')
        post_description = request.form.get('description')
        image_url = request.form.get('image-url')
        prep_time = request.form.get('prep-time')
        
        updated_post = {
            "post_title": post_title,
            "post_description": post_description,
            "user_id": creator,
            "image_url": image_url,
            "prep_time": prep_time,
        }

        posts_collection.update({"_id": ObjectId(post_id)}, updated_post)
        flash("Your post has been updated.", category='success')
        return redirect(url_for("views.profile", username=creator))
        
    post = posts_collection.find_one({"_id": ObjectId(post_id)})
    return render_template("update_post.html", post = post)

# DELETE POST VIEW
@views.route('/delete_post/<post_id>')
def delete_post(post_id):    
    creator = session["user"]   
    posts_collection.delete_one({"_id": ObjectId(post_id)})
    flash("Your post has been deleted.", category='success')
    
    return redirect(url_for("views.profile", username=creator))

# SEARCH BAR VIEW
@views.route("/search", methods=["GET", "POST"])
def search():
    query = request.form.get("query")
    posts = posts_collection.find({"$text": {"$search": query}})
    if posts.count() > 0 :
        return render_template("home.html", posts=posts)
    else:
        flash("No recipes found. Please try again.", category='error')
        return render_template("home.html", posts=posts)