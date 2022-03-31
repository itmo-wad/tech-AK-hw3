from flask import Flask, redirect, url_for, flash
from flask_pymongo import PyMongo

import config
import global_vars

app = Flask(__name__)
app.config["MONGO_URI"] = config.MONGO_URI
app.config['SECRET_KEY'] = config.SECRET_KEY
app.config['UPLOAD_FOLDER'] = config.UPLOAD_FOLDER
mongo = PyMongo(app)

global_vars.init(app_ref=app, mongo_ref=mongo)
import sites.auth, sites.feed, sites.profile, sites.signup

@app.route('/')
def main():
    return redirect(url_for('feed'))

@app.errorhandler(401)
def handle_not_logged_in(e):
    flash("You need to log in to access this page!", "danger")
    return redirect(url_for('auth'))

if __name__ == "__main__":
    # use 0.0.0.0 to make the webpage also accessable for other computers.
    app.run(host='localhost', port=5000, debug=True)
