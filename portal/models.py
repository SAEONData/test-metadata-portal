from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from flask_dance.consumer.storage.sqla import OAuthConsumerMixin

db = SQLAlchemy()


def init_app(app):
    db.init_app(app)


class User(UserMixin, db.Model):
    id = db.Column(db.String, primary_key=True)
    email = db.Column(db.String, unique=True, nullable=False)


class OAuth(OAuthConsumerMixin, db.Model):
    user_id = db.Column(db.String, db.ForeignKey(User.id), nullable=False)
    user = db.relationship(User)
