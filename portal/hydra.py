from .models import db, User, HydraToken
from hydra_client import HydraClientBlueprint

bp = HydraClientBlueprint('hydra', __name__, db, User, HydraToken)


def init_app(app):
    app.register_blueprint(bp)


@bp.local_user_updater
def create_or_update_local_user(user, userinfo):
    if not user:
        user = User(id=userinfo['sub'])
    user.email = userinfo['email']
    return user
