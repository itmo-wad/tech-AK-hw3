from flask import render_template, session

from global_vars import app, mongo
from utilities.login import login_required


@app.route('/profile') #this decerator has to be the first, see: https://stackoverflow.com/questions/47467658/flask-why-app-route-decorator-should-always-be-the-outermost
@login_required
def profile():
    data = mongo.db.users.find_one({"email": session['email']})
    return render_template('profile.html', data=data)