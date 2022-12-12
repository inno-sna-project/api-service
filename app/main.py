import json

from flask import Flask, request
import psycopg2
import os

# postgres database
CREATE_STUDENTS_TABLE = """
CREATE TABLE IF NOT EXISTS students (id SERIAL PRIMARY KEY, first_name TEXT, 
    last_name TEXT, email TEXT, dropped BOOLEAN, drop_reason TEXT);
"""

INSERT_STUDENT = """INSERT INTO students (first_name, last_name, email, dropped, drop_reason) VALUES (%s, %s, %s, %s, 
%s); """

GET_DROPPED_STUDENTS = """SELECT * FROM students WHERE dropped = TRUE;"""

connection = psycopg2.connect(db_name=os.environ["POSTGRES_DB"], user=os.environ["POSTGRES_USER"],
                              password=os.environ["POSTGRES_PASSWORD"], host=os.environ["POSTGRES_HOST"],
                              port=os.environ["DATABASE_PORT"])
app = Flask(__name__)


# {"name": "Room name"}
@app.post("/api/add_dropped_student")
def create_room():
    data = request.get_json()
    first_name = data.get("first_name")
    last_name = data.get("last_name")
    email = data.get("email")
    dropped = True
    drop_reason = data.get("drop_reason")
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(CREATE_STUDENTS_TABLE)
            cursor.execute(INSERT_STUDENT, (first_name, last_name, email, dropped, drop_reason))
            student_id = cursor.fetchone()[0]
    return {"id": student_id, "message": f"Student has been successfully added to dropped students list."}, 201


@app.get("/api/dropped_students")
def get_all_dropped_students(self):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(CREATE_STUDENTS_TABLE)
            cursor.execute(GET_DROPPED_STUDENTS)
            students = cursor.fetchall()

            response = []
            # [{"id":"1","firstName":"first1","lastName":"last1","email":"abc@gmail.com"}]
            for student in students:
                dic = {'id': (student['id'],), 'firstName': (student['first_name'],),
                       'lastName': (student['last_name'],), 'email': (student['email'],)}
                response.append(dic.copy())
            return json.dumps(response, separators=(',', ':'))
