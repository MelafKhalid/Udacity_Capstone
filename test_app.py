import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from app import create_app
from auth import AuthError, requires_auth
from models import setup_db, Actors, Movies


Executive_jwt = {
    'Content-Type': 'application/json',
    'Authorization': os.environ['Executive_jwt']
}

Director_jwt = {
    'Content-Type': 'application/json',
    'Authorization': os.environ['Director_jwt']
}

Assistant_jwt = {
    'Content-Type': 'application/json',
    'Authorization': os.environ['Assistant_jwt']
}


class CapstoneTestCase(unittest.TestCase):
    """This class represents the Capstone test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "capstone_test"
        self.database_path = "postgres://{}/{}".format(
            'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

# Test for each test for successful operation and for expected errors.

# Get test

# Actors

    def test_failed_get_actors(self):
        res = self.client().get('/actors')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

    def test_get_actors(self):
        res = self.client().get('/actors', headers=Assistant_jwt)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertIsNotNone(data['actors'])

# Movie

    def test_failed_get_movies(self):
        res = self.client().get('/movies')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

    def test_get_movies(self):
        res = self.client().get('/movies', headers=Assistant_jwt)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertIsNotNone(data['movies'])

# Post set

# Actors

    def test_failed_post_actors(self):

        res = self.client().post('/actors', json={
            'name': 'Melaf',
            'age': '22',
            'gender': 'female',
            'movie_id': 1
        })

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

    def test_post_actors(self):

        res = self.client().post('/actors', headers=Director_jwt, json={
            'name': 'Melaf',
            'age': '22',
            'gender': 'female',
            'movie_id': 1
        })

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['created'], 1)

# Movies

    def test_failed_post_movies(self):

        res = self.client().post('/movies', json={
            'title': 'Titanic',
            'release_date': '1997-11-18',
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

    def test_post_movies(self):

        res = self.client().post('/movies', headers=Executive_jwt, json={
            'title': 'Titanic',
            'release_date': '1997-11-18',
        })

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['created'], 1)

# Patch Test

# Actors

    def test_failed_patch_actors(self):
        res = self.client().patch('/actors/1', json={
            "name": "Melaf",
            "age": "23",
            "gender": "female"
        })
        data = json.loads(res.data)
        self.assertEqual(data['success'], False)

    def test_patch_actors(self):
        res = self.client().patch('/actors/1', headers=Executive_jwt, json={
            'name': 'Reema'
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertIsNotNone(data['actors'])

# Movie

    def test_failed_patch_movies(self):
        res = self.client().patch('/movies/1', json={
            "title": "Titanic",
            "release_date": "2000-11-18"
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

    def test_patch_movies(self):
        res = self.client().patch('/movies/1', headers=Director_jwt, json={
            'title': 'The Midnight Sky'
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertIsNotNone(data['movies'])

# Delete Test

# Actors

    def test_filed_delete_actors(self):
        res = self.client().delete('/actors/1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

    def test_delete_actors(self):
        res = self.client().delete('/actors/1', headers=Director_jwt)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertIn('delete', data)

# Movies

    def test_failed_delete_movies(self):
        res = self.client().delete('/movies/1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

    def test_delete_movies(self):

        res = self.client().delete('/movies/1', headers=Executive_jwt)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertIn('delete', data)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
