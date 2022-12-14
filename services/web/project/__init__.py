import os

from flask import (
    Flask,
    jsonify,
    send_from_directory,
    request,
    make_response
)
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config.from_object("project.config.Config")
db = SQLAlchemy(app)
CORS(app)


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


def corsify(resp):
    resp.headers["Access-Control-Allow-Origin"] = "*"
    resp.headers["Access-Control-Allow-Headers"] = "*"
    resp.headers["Access-Control-Allow-Methods"] = "*"
    return resp


def _build_cors_preflight_response():
    response = make_response()
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add('Access-Control-Allow-Headers', "*")
    response.headers.add('Access-Control-Allow-Methods', "*")
    return response


@app.route("/api/dropped_students", methods=["GET", "OPTIONS"])
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
                "drop_reason": student.drop_reason,
            }
        )
    return corsify(jsonify(response))


@app.route("/api/add_dropped_student", methods=["POST", "OPTIONS"])
def add_dropped_student():
    if request.method == "OPTIONS":  # CORS preflight
        return _build_cors_preflight_response()
    data = request.get_json()
    first_name = data.get("firstName")
    last_name = data.get("lastName")
    email = data.get("email")
    dropped = True
    # drop_reason = data.get("drop_reason")
    student = Student(first_name, last_name, email, dropped, "")
    db.session.add(student)
    db.session.commit()
    resp = {"id": student.id, "message": "Student has been successfully added to dropped students list."}, 201
    return corsify(jsonify(resp))
