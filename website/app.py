import os
from flask import Flask
from views import views
from auth import auth

if os.path.exists("env.py"):
    import env

# create and configure the app
app = Flask(__name__)

# mapping the secret key from env.py
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")

app.register_blueprint(views, url_prefix="/")
app.register_blueprint(auth, url_prefix="/")

if __name__ == "__main__":
    app.run(
        debug=True, host=os.environ.get("IP"), port=int(os.environ.get("PORT"))
    )
