from locust import HttpUser, task


class FrontUser(HttpUser):
    host = "https://sna.teawide.xyz"
    # host = "http://45.137.190.96"

    @task
    def index(self):
        self.client.get("/")


class BackUser(HttpUser):
    host = "https://snaback.teawide.xyz"
    # host = "http://45.137.190.96:5000"

    @task
    def dropped_students(self):
        self.client.get("/api/dropped_students")
