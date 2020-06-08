from .db import session as db_session
from .models import User, HydraToken
from hydra_oauth2 import HydraOAuth2Blueprint

bp = HydraOAuth2Blueprint('hydra', __name__, db_session, User, HydraToken, 'portal.index')


def init_app(app):
    app.register_blueprint(bp)


def get_access_token():
    return bp.get_access_token()


@bp.local_user_updater
def create_or_update_local_user(user, userinfo):
    if not user:
        user = User(id=userinfo['sub'])
    user.email = userinfo['email']
    return user
