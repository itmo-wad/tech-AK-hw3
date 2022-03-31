from flask import render_template, request, flash, url_for, redirect, session, jsonify, make_response
from jwcrypto import jwk, jwt
from werkzeug.security import check_password_hash

from global_vars import app, mongo


def send_auth_token():
    """ Not used anymore, using Flask's built-in session cookie"""
    # See: https://jwcrypto.readthedocs.io/en/latest/jwt.html
    # Create a symmetric key using for signing the token
    # Use _oct_et key pair (Edwards curve keys), RSA and so on also possible
    key = jwk.JWK(generate='oct', size=256)

    # Create a signed token with the generated key
    Token = jwt.JWT(header={"alg": "HS256"},
                    claims={"info": "I'm a signed token"})
    Token.make_signed_token(key)
    # Token.serialize() #Display token as output

    # Further encrypt the token with the same key
    Etoken = jwt.JWT(header={"alg": "A256KW", "enc": "A256CBC-HS512"},
                     claims=Token.serialize())
    Etoken.make_encrypted_token(key)

    return jsonify({'token': Etoken.serialize()})


@app.route('/auth', methods=['GET', 'POST'])
def auth():
    if request.method == "GET":
        return render_template('auth.html')
    else:
        email = request.form['email']
        passwd = request.form['pass']

        query = mongo.db.users.find_one({"email": email})
        if query is not None and 'password' in query:
            hash_passwd = query['password']
            if check_password_hash(hash_passwd, passwd):
                # Generate new session ID
                # Note: Flask already handles one special session cookie per user and signs it cryptographically.
                # I. e., we just need to set the username of the current user in the session,
                # the other things (prevent from giving the same session to the users, encrypt the sessionID, store
                # the session on the server and so on) Flask will handle for us!
                session['email'] = email
                return redirect(url_for('feed'))

        # Else no match in database
        flash('Wrong e-mail or password!', 'warning')
        return render_template('auth.html')


def create_new_session(email):
    """ Not used anymore, using Flask's built-in session cookie"""
    while True:
        sessionID = "abc" # implement here some hasing algorithm which takes the current time, a secret value, the username and other parameters to create a hash which will be definetely unique.
        session['sessionID'] = sessionID

        mongo.db.sessions.insert_one({"sessionID": sessionID, "email": email})

        resp = make_response()
        resp.set_cookie('sessionID', sessionID)
        return resp


