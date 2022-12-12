from flask.cli import FlaskGroup

from project import app, db, Student
from project.utils import generate_students

cli = FlaskGroup(app)


@cli.command("create_db")
def create_db():
    db.drop_all()
    db.create_all()
    db.session.commit()


@cli.command("seed_db")
def seed_db():
    for student in generate_students(10):
        db.session.add(Student(**student))
    db.session.commit()


if __name__ == "__main__":
    cli()
