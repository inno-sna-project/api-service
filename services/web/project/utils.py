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
    drop_reasons = ["Human Instrumentality Project", "Third Impact", "Frozen to death sleeping in university dorms", 
        "Poisoned by Shinji Ikari", "Exploded after following Gendo Ikari into the LCL", "Died of a broken heart after Asuka Langley Soryu died", 
        "Reached the form of god and ascended to heaven", "Turned himself into a Gigachad by watching too much anime", "Best Genchin Impact player"]
    for _ in range(num_students):
        dropped = random.random() < 0.4
        student = {
            "firstName": random_first_name(),
            "lastName": random_last_name(),
            "email": random_email(),
            # dropped with 10% probability
            "dropped": dropped,
            # if dropped, drop reason is random
            "drop_reason": random.choice(drop_reasons) if dropped else "N/A"
        }
        students.append(student)
    return students
