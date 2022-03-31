import datetime
import os
import random

from flask import flash
from werkzeug.utils import secure_filename

import config
from global_vars import app


def is_file_allowed(filename):
    return ('.' in filename) and (filename.rsplit('.', 1)[1].lower() in config.ALLOWED_EXTENSIONS)

def handleImageUpload(request, name_of_field, create_flask=True):
    """Checks if the image is not malicious and if not, saves the image. Returns the new filename or, in case of errors, an empty string."""

    if name_of_field not in request.files:
        if create_flask:
            flash('No file provided', 'danger')
        return ""

    file = request.files[name_of_field]

    if file.filename == '':
        if create_flask:
            flash('No file selected', 'danger')
        return ""

    if not is_file_allowed(file.filename):
        if create_flask:
            flash('Invalid file extension', 'danger')
        return ""

    if file:
        filename = secure_filename(file.filename)
        # Set random filename, otherwise user could overwrite each other
        filename = datetime.datetime.now().strftime('%m-%d-%Y-%H-%M-%S') + '_' + str(random.randint(100, 999)) + '_' + filename
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return filename

    return ""