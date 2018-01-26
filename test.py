# coding=utf-8

import unittest
import app
import requests
import json
import sys


class TestFlaskApiUsingRequests(unittest.TestCase):
    def test_todos_list_resource_get(self):
        self.maxDiff = None
        response = requests.get('http://localhost:5000/todos')

        expectedResponse = [
                {
                    "id": 1,
                    "task": "'Write Unit Tests'",
                    "uri": "http://localhost:5000/todos/1"
                },
                {
                    "id": 2,
                    "task": "'Write Unit Tests'",
                    "uri": "http://localhost:5000/todos/2"
                },
                {
                    "id": 3,
                    "task": "Testing via curl",
                    "uri": "http://localhost:5000/todos/3"
                },
                {
                    "id": 4,
                    "task": "Testing via curl",
                    "uri": "http://localhost:5000/todos/4"
                }
        ]

        self.assertEqual(response.json(), expectedResponse)


class TestFlaskApi(unittest.TestCase):
    def setUp(self):
        self.app = app.app.test_client()

    def test_todos_list_resource_post(self):
        response = self.app.get('/todos')
        self.assertEqual(json.loads(response.get_data().decode(sys.getdefaultencoding())), {'hello': 'world'})


if __name__ == "__main__":
    unittest.main()
