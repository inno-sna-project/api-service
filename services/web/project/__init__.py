import os

from flask import (
    Flask,
    jsonify,
    send_from_directory,
    request,
)
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config.from_object("project.config.Config")
db = SQLAlchemy(app)


class Student(db.Model):
    __tablename__ = "students"

    id = db.Column(db.Integer, primary_key=True)
    firstName = db.Column(db.String(128), nullable=False)
    lastName = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(128), unique=True, nullable=False)
    dropped = db.Column(db.Boolean, nullable=False, default=False)
    drop_reason = db.Column(db.String(128), nullable=True)

    def __init__(self, firstName, lastName, email, dropped=False, drop_reason="N/A"):
        self.firstName = firstName
        self.lastName = lastName
        self.email = email
        self.dropped = dropped
        self.drop_reason = drop_reason


@app.get("/api/dropped_students")
def get_all_dropped_students():
    students = Student.query.filter_by(dropped=True).all()
    response = []
    for student in students:
        response.append(
            {
                "id": student.id,
                "firstName": student.firstName,
                "lastName": student.lastName,
                "email": student.email,
            }
        )
    return jsonify(response)


@app.post("/api/add_dropped_student")
def add_dropped_student():
    data = request.get_json()
    first_name = data.get("first_name")
    last_name = data.get("last_name")
    email = data.get("email")
    dropped = True
    drop_reason = data.get("drop_reason")
    student = Student(first_name, last_name, email, dropped, drop_reason)
    db.session.add(student)
    db.session.commit()
    return jsonify({"id": student.id, "message": "Student has been successfully added to dropped students list."}), 201
