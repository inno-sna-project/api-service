import random
import string
import names


# generate a random email address
def random_email():
    return "".join(random.choice(string.ascii_lowercase) for i in range(10)) + "@example.com"


# generate a random first name using names library
def random_first_name():
    return names.get_first_name()


def random_last_name():
    return names.get_last_name()


def generate_students(num_students):
    students = []
    for _ in range(num_students):
        dropped = random.random() < 0.1
        student = {
            "firstName": random_first_name(),
            "lastName": random_last_name(),
            "email": random_email(),
            # dropped with 10% probability
            "dropped": dropped,
            # if dropped, drop reason is random
            "drop_reason": random.choice(["N/A", "no time", "too hard"]) if dropped else "N/A",
        }
        students.append(student)
    return students
