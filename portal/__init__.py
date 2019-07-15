from flask import Flask
from flask_login import LoginManager

from . import models, views, cli, config, hydra

app = Flask(__name__)
app.config.from_object(config.Config)

models.init_app(app)
views.init_app(app)
cli.init_app(app)
hydra.init_app(app)

login_manager = LoginManager()
login_manager.login_view = 'hydra.login'
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return models.User.query.get(user_id)
