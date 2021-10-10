import unittest
from flask import json
from app import app 

class KeyStoreTest(unittest.TestCase):
    def test_set(self):
        tester = app.test_client(self)
        response = tester.post("set", data=json.dumps({"hello": "world"}), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(b'hello' in response.data)
    def test_get(self):
        tester = app.test_client(self)
        response = tester.get("get/key1")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(b'value1' in response.data)
    def test_search(self):
        tester = app.test_client(self)
        response = tester.get("search?prefix=key")
        self.assertEqual(response.status_code, 200)



if __name__ == "__main__":
    unittest.main()


