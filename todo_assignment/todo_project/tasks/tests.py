from django.test import TestCase, Client
import json

class TaskAPITest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_create_task(self):
        response = self.client.post(
            "/api/tasks/",
            data=json.dumps({"title": "Test Task"}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 201)

    def test_get_tasks(self):
        response = self.client.get("/api/tasks/")
        self.assertEqual(response.status_code, 200)
