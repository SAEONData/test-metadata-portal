from flask_login import UserMixin
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String

from hydra_oauth2 import HydraTokenMixin

Base = declarative_base()


def init_app(app):
    from .db import session

    # ensure that the db session is closed and disposed after each request
    @app.teardown_appcontext
    def discard_session(exc):
        session.remove()


class User(UserMixin, Base):
    __tablename__ = 'user'
    id = Column(String, primary_key=True)
    email = Column(String, nullable=False)


class HydraToken(HydraTokenMixin, Base):
    pass
