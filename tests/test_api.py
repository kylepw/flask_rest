"""
    test_api.py
    ~~~~~~~~~~~

    Test API JSON requests/responses.

"""
from flask_rest import app, mongo
import unittest

class TestErrorHandling(unittest.TestCase):
    def setUp(self):
        self.root = '/api'
        self.app = app.test_client()
        self.app.testing = True

    def test_get_all_docs(self):
        re = self.app.get(self.root + '/')
        self.assertEqual(re.status_code, 200)
        self.assertTrue(re.is_json)
        self.assertLess(max(len(re.get_json()), 20), 21)

    def test_nonexistent_endpoint(self):
        re = self.app.get(self.root + '/jeezus')
        self.assertTrue(re.is_json)
        self.assertEqual(re.status_code, 404)

    @unittest.SkipTest
    def test_valid_json_post(self):
        re = self.app.post(self.root + '/', json=dict(name='hey'))
        self.assertEqual(re.status_code, 200)
        self.assertTrue(re.is_json)

    @unittest.SkipTest
    def test_invalid_json_post(self):
        re = self.app.post(self.root + '/', json=dict(greeting='hey'))
        self.assertEqual(re.status_code, 400)
        self.assertIn('name field required', re.get_json()['errors'][0]['message'])

    def test_valid_patch(self):
        inserted_id = mongo.db.osaka.insert_one({"name": "hello world"}).inserted_id
        self.assertIsNotNone(mongo.db.osaka.find_one({"_id": inserted_id}))

        self.assertIsNone(mongo.db.osaka.find_one({"_id": inserted_id, "instrument": {"$exists": True } }))
        self.app.patch(self.root + '/' + str(inserted_id), json=dict(instrument='drums'))
        self.assertIsNotNone(mongo.db.osaka.find_one({"_id": inserted_id, "instrument": {"$exists": True } }))

        mongo.db.osaka.delete_one({"_id": inserted_id})
        self.assertIsNone(mongo.db.osaka.find_one({"_id": inserted_id}))

