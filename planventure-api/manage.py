from flask.cli import FlaskGroup
from app import app, db

cli = FlaskGroup(app)


@cli.command("create_db")
def create_db():
    """Creates the database tables."""
    db.create_all()
    print("Database tables created!")


@cli.command("drop_db")
def drop_db():
    """Drops the database tables."""
    db.drop_all()
    print("Database tables dropped!")


if __name__ == "__main__":
    cli()
