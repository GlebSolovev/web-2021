import random
import time

from locust import HttpUser, task, between


class TestUser(HttpUser):
    wait_time = between(1, 5)  # seconds

    def on_start(self):
        response = self.client.post("/new-user", json={"name": "test user", "wish": "i want to load test"})
        self.secret_key = response.json()["secret_key"]

    @task(2)
    def check_happy_person(self):
        self.client.get("/happy-person")
        time.sleep(3)

    @task(2)
    def check_user_profile(self) -> int:
        self.client.request_name = "check user profile"
        balance = self.client.get("/user/" + self.secret_key).json()["balance"]
        time.sleep(2)
        return balance

    @task(1)
    def support_happy_person(self):
        balance = self.check_user_profile()
        if balance < 1:
            return
        coins = random.randint(1, balance)
        self.client.request_name = "support happy person"
        self.client.post("/user/" + self.secret_key + "/support/" + str(coins))
