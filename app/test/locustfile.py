import random
import time

from locust import HttpUser, task, between


class TestUser(HttpUser):
    wait_time = between(1, 5)  # seconds

    def on_start(self):
        response = self.client.post("/new-user", json={"name": "test user", "wish": "i want to load test"})
        self.secret_key = response.json()["secret_key"]

    @task
    def check_happy_person(self):
        self.client.get("/happy-person")
        time.sleep(1)

    @task
    def check_user_profile(self) -> int:
        response = self.client.get("/user/" + self.secret_key)
        time.sleep(1)
        return response.json()["balance"]

    @task(3)
    def support_happy_person(self):
        balance = self.check_user_profile()
        if balance < 1:
            return
        coins = random.randint(1, balance)
        self.client.post("/user/" + self.secret_key + "/support/" + str(coins))
