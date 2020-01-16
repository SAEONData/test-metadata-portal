import click
from flask.cli import with_appcontext


def init_app(app):
    app.cli.add_command(init_db)


@click.command('initdb')
@click.option('--drop-all', is_flag=True)
@with_appcontext
def init_db(drop_all):
    """
    Create tables used by this app.
    :param drop_all: if this flag is set, drop all tables first, before issuing create table commands
    """
    from .db import engine
    from .models import Base, User, HydraToken

    if drop_all:
        Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    click.echo("Initialized the database.")
