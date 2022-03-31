from functools import wraps

from flask import session, abort


def login_required(func):
    # This helper function is needed when using url_for function,
    # otherwise this wrapper returns his function name and not the previous function name so that url_for cannot find it
    # see: https://stackoverflow.com/questions/14114296/why-does-flasks-url-for-throw-an-error-when-using-a-decorator-on-that-item-in-p
    @wraps(func)
    def is_user_logged_in():
        if 'email' not in session:
            abort(401) #unauthorized
        return func()

    return is_user_logged_in