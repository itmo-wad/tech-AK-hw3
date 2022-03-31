# This module holds all global variables.

app = None
mongo = None


def init(app_ref, mongo_ref):
    global app
    app = app_ref
    global mongo
    mongo = mongo_ref
