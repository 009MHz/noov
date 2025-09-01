from locust import HttpUser, task, between

class WebApiUser(HttpUser):
    wait_time = between(1, 3)

    @task
    def health(self):
        self.client.get("/health")

# locust -f perf/locustfile.py --headless -u 50 -r 5 -t 5m --host https://api.example.com --csv=reports/locust