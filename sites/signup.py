import datetime

from flask import render_template, request, flash, url_for, redirect
from werkzeug.security import generate_password_hash

import config
from global_vars import app, mongo
from utilities.image_upload import handleImageUpload


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == "GET":
        return render_template('signup.html')
    else:
        name = request.form['name']
        passwd = request.form['pass']
        github = request.form['github']
        university = request.form['university']
        email = request.form['email']

        # An if actually works by computing a value for the logical expression you give it: True or False. If you simply use a variable name (or a literal string like "hello") instead of a logical test, the rule is: An empty string counts as False, all other strings count as True. Empty lists and the number zero also count as false, and most other things count as true.
        # Check if all fields are filled
        if not (name and passwd and name and github and university and email):
            flash('Please fill in all fields', 'warning')
            return render_template('signup.html')

        # Check if name is already registered
        if mongo.db.users.find_one({"email": email}): #true, if there was one entry found in database
            flash('This name is already registered. Do you want to go to the <a href="' + url_for("auth") + '">authentication page</a>?', 'warning')
            return render_template('signup.html')

        # Check if with image file is everything okay and process image file
        filename = handleImageUpload(request=request, name_of_field='fileID')
        if not filename:
            # there was an error, reload page to show flask message
            return render_template('signup.html')

        # Fall-through, if no if condition above is met, we can add the entry.
        hashed_passwd = generate_password_hash(passwd)
        mongo.db.users.insert_one({"email": email, "password": hashed_passwd, "pic_file_name": filename, "fullname": name, "github": github, "github_url": config.GITHUB_PROFILE_PAGE_URL + github, "university": university, "creation_date": datetime.date.today().strftime('%d.%m.%Y')})

        # Check if inserting has worked
        if mongo.db.users.find_one({"email": email}):
            #adding new name to database has worked
            flash('Successfully registered! Please log in with your new access credentials', 'success')
            return redirect(url_for('auth'))
        else:
            flash('Something went wrong. Try again', 'warning')
            return render_template('signup.html')