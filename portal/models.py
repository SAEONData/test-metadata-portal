from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

from hydra_client import HydraTokenMixin

db = SQLAlchemy()


def init_app(app):
    db.init_app(app)


class User(UserMixin, db.Model):
    id = db.Column(db.String, primary_key=True)
    email = db.Column(db.String, nullable=False)


class HydraToken(HydraTokenMixin, db.Model):
    pass
