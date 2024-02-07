from core import *
from .utils import *
from urllib.parse import quote_plus, urlencode
from authlib.integrations.flask_client import OAuth, OAuthError
from flask import Blueprint, redirect, session, url_for, current_app, request

user_login = Blueprint('login', __name__)

oauth = OAuth(current_app)

oauth.register(
    'auth0',
    client_id = auth0client_id,
    client_secret = auth0client_secret,
    client_kwargs={
        'scope': 'openid profile email',
    },
    server_metadata_url=f'https://{auth0domain}/.well-known/openid-configuration'
)


@user_login.route('/login/')
def login():
    us = request.args.get('us')
    if session.get('token'):
        return redirect(us)
    return oauth.auth0.authorize_redirect(
        redirect_uri=url_for('login.callback', us=us, _external=True)
    )

@user_login.route('/callback/', methods=['GET', 'POST'])
def callback():
    us = request.args.get('us')
    if session.get('token'):
        return redirect(us)
    try:
        token = oauth.auth0.authorize_access_token()
    except OAuthError as e:
        return f'Error: {e.description}'
    loginhandler.registerLogin(token)
    return redirect(us)

@user_login.route('/logout/')
def logout():
    loginhandler.registerLogout()
    return redirect(
        'https://pritam20ps05.us.auth0.com/v2/logout?'
        + urlencode(
            {
                'returnTo': url_for('home', _external=True),
                'client_id': auth0client_id,
            },
            quote_via=quote_plus,
        )
    )
