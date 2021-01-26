import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from app import create_app
from auth import AuthError, requires_auth
from models import setup_db, Actors, Movies


Executive_jwt = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InFvdnZLQ1h6ekMya21NMDhycVFKMSJ9.eyJpc3MiOiJodHRwczovL2ZzbmQtbWVsYWYudXMuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDYwMDFlNGUzMTMwOWUzMDA2OWM0ODliNyIsImF1ZCI6IkNhcHN0b25lIiwiaWF0IjoxNjExNjA0ODcxLCJleHAiOjE2MTE2OTEyNzEsImF6cCI6InkxS3pMbm9rQUw3b2RZRzNKc0ZRNlVlRnJSNUE4UnNUIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3JzIiwiZGVsZXRlOm1vdmllcyIsImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIiwicGF0Y2g6YWN0b3JzIiwicGF0Y2g6bW92aWVzIiwicG9zdDphY3RvcnMiLCJwb3N0Om1vdmllcyJdfQ.gjf8SFHv6svl6bfHOi7D-BwphnUK2LexO0gX_MhkbRAOxI2BTl5N3R0bXJKULg2y_jLreQehAm5DGj1LN5uX2iWJ33dcBKw6UHJNJY4fHxLCtjyf51JAQ5L60aTqci1E7RR5jli2jUNs43pWFJ6ITiUnmrU3GHmgy5FrUAK9V7es8IaLKB6UGXgVYGfRG_6M4sRbRR8FbtVmMzb1OAishomI2MVEc31-d0gnUQwUh8i4epLYrcVSunfidGFITNY1XEz5ll_Hoyhaov3e16yTULysCa-kljsbmcuO59GjYq39L4ca9Eo_ZlXMFlyBNKsXJyZWvTm4H2dU5gE4GiQaUA'}

Director_jwt = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InFvdnZLQ1h6ekMya21NMDhycVFKMSJ9.eyJpc3MiOiJodHRwczovL2ZzbmQtbWVsYWYudXMuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDYwMDIxMzljYjEzZTU3MDA3Njg2YzVkNyIsImF1ZCI6IkNhcHN0b25lIiwiaWF0IjoxNjExNjA0Nzg0LCJleHAiOjE2MTE2OTExODQsImF6cCI6InkxS3pMbm9rQUw3b2RZRzNKc0ZRNlVlRnJSNUE4UnNUIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3JzIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvcnMiLCJwYXRjaDptb3ZpZXMiLCJwb3N0OmFjdG9ycyJdfQ.DxEqmajyYoZBW4-udMkhdhKkyDW75Kntdq5uFdKQM27iJEUvcw9QV7TObHLn7WBJp4sB3gv-1UkMpQN_VThLgrRqb1OcK1-a8HOXDjT8v5NII-mG73sUNMDzUvjKWxvVlo5OIp0wm5wVSmArRmnL8cLNmoFTzJOg4WUrNH4xWl0SfXp9TB_hqfjtf8LtNVgToVZNbhY72i5K4GZ3sihm-lYVGLUTZJnB5wLNxMvaK9FQpi6AVl5F5EFcyqWm2vz8yF8ApU3hHV9_q7yMEzJenw9S9I5jgO-uJvnHdV04F3mtEzYl_eimn5EJnHyLC_KvVD3HnNvny2KrORfI2hpxhg'}

Assistant_jwt = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InFvdnZLQ1h6ekMya21NMDhycVFKMSJ9.eyJpc3MiOiJodHRwczovL2ZzbmQtbWVsYWYudXMuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDYwMGYyNDRhMzQwMjg1MDA3MTYwNWIzYyIsImF1ZCI6IkNhcHN0b25lIiwiaWF0IjoxNjExNjA1MTI0LCJleHAiOjE2MTE2OTE1MjQsImF6cCI6InkxS3pMbm9rQUw3b2RZRzNKc0ZRNlVlRnJSNUE4UnNUIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyJdfQ.sEAU_h2xRPEVc5i7hA4THUTTNd-KuiWB1I4QymbEU1-HMK0xuFUx5tyKP39aypxxv0Qejom_4sNkn8kR2QcS4Z4zSbTVTdzQC7p61hMTTkGsq7OCF5G7x5TSp-QpWUdLXOWJz_ZteuPlrpzNgg7KYX7t7P4nBVIMd2qs37T9H7JOH71sCeV3FFaoV5mcQHc6yaTmxNOEmm0BGnW-by44tBYZ-r-WZM-bMPA7UnigRhH_rgiEGQLyphF0xekn84Md2QPl2XQVaySYyi4wYbmh2PFStcp88RG9op_OoOkjG-xjj5XFzxazo1CbxCv1_1C9D07na0LuHzYSlBcXYR6s4A'}

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