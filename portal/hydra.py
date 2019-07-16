from .models import db, User, HydraToken
from hydra_client import HydraClientBlueprint

bp = HydraClientBlueprint('hydra', __name__, db, User, HydraToken)


def init_app(app):
    app.register_blueprint(bp)


@bp.local_user_creator
def create_local_user(userinfo):
    return User(id=userinfo['sub'], email=userinfo['email'])
