import logging
import traceback
from flask import Flask, request, g, Response
from flask_cors import CORS
from functools import wraps
from plynx.db.user import User
from plynx.utils.config import get_config
from plynx.utils.common import JSONEncoder
from plynx.utils.db_connector import check_connection

app = Flask(__name__)

DEFAULT_USERNAME = 'default'
DEFAULT_PASSWORD = ''

_config = None


def verify_password(username_or_token, password):
    if _config and _config.auth.secret_key and username_or_token == DEFAULT_USERNAME:
        return False
    user = User.verify_auth_token(username_or_token)
    if not user:
        # try to authenticate with username/password
        user = User.find_user_by_name(username_or_token)
        if not user or not user.verify_password(password):
            return False
    g.user = user
    return True


def authenticate():
    # 401 response
    return Response(
        'Could not verify your access level for that URL; You have to login with proper credentials',
        401,
        {'WWW-Authenticate': 'PlynxBasic realm="Login Required"'}
    )


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth:
            # if auth not provided, try default
            auth = {'username': DEFAULT_USERNAME, 'password': DEFAULT_PASSWORD}
        if not verify_password(auth['username'], auth['password']):
            return authenticate()
        return f(*args, **kwargs)
    return decorated


def register_user(username, password):
    """Register a new user.

    Args:
        username    (str):  Username
        password    (str):  Pasword

    Return:
        (str):  None if success, or error message if failed
    """
    if username is None or password is None:
        return 'Missing username or password'

    if User.find_user_by_name(username):
        return 'User with name `{}` already exists'.format(username)

    user = User()
    user.username = username
    user.hash_password(password)
    user.save()
    return None


def _init_default_user():
    if not User.find_user_by_name(DEFAULT_USERNAME):
        message = register_user(DEFAULT_USERNAME, DEFAULT_PASSWORD)
        if message:
            raise Exception(message)
        logging.info('Created default user `{}`'.format(DEFAULT_USERNAME))
    else:
        logging.info('Default user `{}` already exists'.format(DEFAULT_USERNAME))


def make_fail_response(message):
    return JSONEncoder().encode({
        'status': 'failed',
        'message': message
    })


def make_success_response(message='Completed', **extra_response):
    return JSONEncoder().encode(dict(
        {
            'status': 'success',
            'message': message,
        }, **extra_response))


def handle_errors(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            app.logger.error(traceback.format_exc())
            return make_fail_response('Internal error: "{}"'.format(repr(e))), 500
    return decorated


def run_api():
    global _config
    _config = get_config()

    check_connection()

    # Create default user if in single user mode
    if not _config.auth.secret_key:
        logging.info('Single user mode')
        _init_default_user()
    else:
        logging.info('Multiple user mode')

    CORS(app, resources={r"/*": {"origins": "*"}})
    app.run(
        host=_config.web.host,
        port=_config.web.port,
        debug=_config.web.debug,
        use_reloader=False,
    )
