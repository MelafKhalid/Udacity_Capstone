import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from app import create_app
from auth import AuthError, requires_auth
from models import setup_db, Actors, Movies


Executive_jwt = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InFvdnZLQ1h6ekMya21NMDhycVFKMSJ9.eyJpc3MiOiJodHRwczovL2ZzbmQtbWVsYWYudXMuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDYwMDFlNGUzMTMwOWUzMDA2OWM0ODliNyIsImF1ZCI6IkNhcHN0b25lIiwiaWF0IjoxNjExNjg4MjU5LCJleHAiOjE2MTE3NzQ2NTksImF6cCI6InkxS3pMbm9rQUw3b2RZRzNKc0ZRNlVlRnJSNUE4UnNUIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3JzIiwiZGVsZXRlOm1vdmllcyIsImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIiwicGF0Y2g6YWN0b3JzIiwicGF0Y2g6bW92aWVzIiwicG9zdDphY3RvcnMiLCJwb3N0Om1vdmllcyJdfQ.KX8lZ-LqzF0_bbw-kJ-lbYxjnwGis2EZ8N49UTDkyZHvKqRtRuCgaesBjrhZVyqUAMCPKZc90rNjuqv-Z7TvK3HfOfRr5MOZdZpUDqts2aGE4OQFJSxzf2l7IEdYLYoW_YzrBOhbxQfYjoSRMa36lvA7iPMNIK1tYCnEqJuS6l8Jl6KJDkJItzHaY7rqHkLZJw-DAuH4h4cxaFif8u66GE0qyFC51kE2tD4hIqZAsKYmardKl5Bh3j9XDTMxUJsWmIZPUFOqd33Zj2guA-k3s3lJN2ROioYdK-1MWGhyhun8Crtw3WwVa2Lxcy5jn7q2q2Da5cnQhTOF-QdQIsJ-lw'}

Director_jwt = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InFvdnZLQ1h6ekMya21NMDhycVFKMSJ9.eyJpc3MiOiJodHRwczovL2ZzbmQtbWVsYWYudXMuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDYwMDIxMzljYjEzZTU3MDA3Njg2YzVkNyIsImF1ZCI6IkNhcHN0b25lIiwiaWF0IjoxNjExNjg4MzM3LCJleHAiOjE2MTE3NzQ3MzcsImF6cCI6InkxS3pMbm9rQUw3b2RZRzNKc0ZRNlVlRnJSNUE4UnNUIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3JzIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvcnMiLCJwYXRjaDptb3ZpZXMiLCJwb3N0OmFjdG9ycyJdfQ.aBVsFthdhqE1vnmWNKjglZwlAlNasZ-n7s6h438C7Ah0IkfN1_vQa_oipP-U8BLUk7BHYgt9HdGi11budlOQEZ2d8LgKZGqIGE02CyBsn-uBS2hphsh5bmQLZbIxuVIaqcgDthq205IU8VFnhkJKd5XWsaa0Wk0t_3BTbdA_o2FEWwqg5pPo5xVRLVICtCNSrQwOoPtBcphPBGUMzjjzG48MP6es22xGQs43wHHqNKiMzxAayX2PR90OUVKnT2UHwnDkGct6ZTo5prdUHwr8Q-75CLwMPD6eaicJFEflOYgG2p6CQ00C5puRasC7-aWrBHcsx33MkfwX89gmZJ7gcw'}

Assistant_jwt = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InFvdnZLQ1h6ekMya21NMDhycVFKMSJ9.eyJpc3MiOiJodHRwczovL2ZzbmQtbWVsYWYudXMuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDYwMGYyNDRhMzQwMjg1MDA3MTYwNWIzYyIsImF1ZCI6IkNhcHN0b25lIiwiaWF0IjoxNjExNjg4NDE2LCJleHAiOjE2MTE3NzQ4MTYsImF6cCI6InkxS3pMbm9rQUw3b2RZRzNKc0ZRNlVlRnJSNUE4UnNUIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyJdfQ.pHXlBzFj3oh6-Q6ogum3gsYGxrOqo9HxQv95KD53KLpC-8qHPwC4hO_XDv6RZeZc76JYU2l8GleOOuxQCqI9rrTaA2eUzq_VBcA8QrAZ0CMMVQroR-6HFLxyu30Yaf4HqFu9wb1v7OaWBmwOdwvpLb_t-RM8zO0pgni23_vgL6f95dUVyFtfBkOXYiOjUqVLrkc-1HTiJqoRBjiYwOUjprT7VcmH_dkKk2Xtr_9HM6MiDKWVnXVpEUZSjapRLDvXM6Nh2Ydkp4RybA_8DdtZzDrkNzbpyclph3rjq6iT7hcMZqEFU8DPrgKZ-EnxOyZGaV7QntH_gjZStbvOHpR40w'}

class CapstoneTestCase(unittest.TestCase):
    """This class represents the Capstone test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "capstone_test"
        self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)
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