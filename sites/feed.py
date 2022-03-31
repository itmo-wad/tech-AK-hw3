import datetime

from flask import render_template, session, redirect, url_for, abort, request

import config
from global_vars import app, mongo
from utilities.image_upload import handleImageUpload


class Post:
    def __init__(self, name, author_profile_pic, time, text, pic):
        self.name = name #in python, these instance variable directly exist and do not need to be declared
        self.author_profile_pic = author_profile_pic
        self.time = time
        self.text = text
        self.pic = pic


@app.route('/feed', methods=['GET', 'POST'])
def feed():
    if request.method == "GET":
        #this find query matches every entries and gives the last posts to the user
        posts = mongo.db.posts.find({}).sort("time",-1).limit(config.NUMBER_OF_SHOWN_POSTS)

        #data = mongo.db.users.find_one({"email": session['email']})
        return render_template('feed.html', posts=posts, user_authenticated='email' in session)

    else:
        text = request.form['text']

        # Check if with image file is everything okay and process image file
        img_filename = handleImageUpload(request=request, name_of_field='fileID', create_flask=False)


        #Get user data
        if 'email' not in session:
            abort(401)

        email = session['email']
        userdata = mongo.db.users.find_one({"email": email})

        mongo.db.posts.insert_one({"name": userdata['fullname'], "author_profile_pic": userdata['pic_file_name'], "time": datetime.datetime.now(), "display_time": datetime.datetime.now().strftime('%d.%m.%Y %H:%M'), "text": text, "pic": img_filename})


        return redirect(url_for('feed'))