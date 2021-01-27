import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from app import create_app
from auth import AuthError, requires_auth
from models import setup_db, Actors, Movies


Executive_jwt = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InFvdnZLQ1h6ekMya21NMDhycVFKMSJ9.eyJpc3MiOiJodHRwczovL2ZzbmQtbWVsYWYudXMuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDYwMTExNmUwM2IyZDM0MDA2OWQwYWVlOSIsImF1ZCI6IkNhcHN0b25lIiwiaWF0IjoxNjExNzMyODYxLCJleHAiOjE2MTE4MTkyNjEsImF6cCI6InkxS3pMbm9rQUw3b2RZRzNKc0ZRNlVlRnJSNUE4UnNUIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3JzIiwiZGVsZXRlOm1vdmllcyIsImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIiwicGF0Y2g6YWN0b3JzIiwicGF0Y2g6bW92aWVzIiwicG9zdDphY3RvcnMiLCJwb3N0Om1vdmllcyJdfQ.rVpZHC6FxMkEE2to-9ZucEJWpjmDzTkA4o_onoOOgmCjrXFTd8EAvOU8zjWm2X3bU0HLHVA-klr9GMG9D4Flspr_XOqg2ydgaZH7nvKsUGcnUq_NHEZkHI9ep0YCNVOfhQ9KnUHErRygPEWTa2fCXvn3bzwNj4hBnGBZ_mVCbo1x9GdtRatwOEDJJDOTQwPkmCKNNllgcvtHAGA84E67c7P-6PXoCD2XEpPeltWjW9s2A0d4RmA92YZILdS2rmPcx0tBgk_w81UdkrOABu6eqiCP7tAxxoIDbhfXsYaHYcFECXxb4RWvTtZm_iB5hNe-WxZ5hyAxgJKxabs-qTL3gA'}

Director_jwt = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InFvdnZLQ1h6ekMya21NMDhycVFKMSJ9.eyJpc3MiOiJodHRwczovL2ZzbmQtbWVsYWYudXMuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDYwMTExNDliMzQwMjg1MDA3MTYwODEzOCIsImF1ZCI6IkNhcHN0b25lIiwiaWF0IjoxNjExNzMyNTcxLCJleHAiOjE2MTE4MTg5NzEsImF6cCI6InkxS3pMbm9rQUw3b2RZRzNKc0ZRNlVlRnJSNUE4UnNUIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3JzIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvcnMiLCJwYXRjaDptb3ZpZXMiLCJwb3N0OmFjdG9ycyJdfQ.p1hFhBP5B-XErwVtqUMSynPeHUtEyqrBC_tTcugK5xkmZQNNQGMUtP23I59DljmRZ6lHUBzzlBsTXu05Zs8VpfORLNIWaT2wX-ILH-yiKCQ2YYCChM2QRZiw6pfyKkF_PnryE1_PLc34hIKjzBuIladRFnGVE0oODW05fsU73Qvap68I-VfedURGlZMRMijc_0V14vD-EykQb8W1TcEz0E6ziuHz-KfdRLR-iYzB8Z0a8L_X4vwuTwSwikhvAx7mO8FFsLkqPXn_qUo2uyx6nlrcT1gO92t8Yc5CLem5oPzbYFgsHCgD1bAc0qPcS4rak197M9DRvco6868u0PzeoA'}

Assistant_jwt = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InFvdnZLQ1h6ekMya21NMDhycVFKMSJ9.eyJpc3MiOiJodHRwczovL2ZzbmQtbWVsYWYudXMuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDYwMTExMTM1NDQxZmQ2MDA3MDgyM2Q2MyIsImF1ZCI6IkNhcHN0b25lIiwiaWF0IjoxNjExNzMxODUwLCJleHAiOjE2MTE4MTgyNTAsImF6cCI6InkxS3pMbm9rQUw3b2RZRzNKc0ZRNlVlRnJSNUE4UnNUIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyJdfQ.uq8LstnH8fqJ28Cj0rDnQ_NdmHtBy0j-T0c64PQlrvgx_JUrrjtQvsFi4TNmqSRTTtp4gyQuIOC5aY6jsHVAw_Hr8v2R4XurxxnVoJWvbwN2jrxu-ua36cCR9Y8Yc7r1YY06L4TKpH0HddRJiqFsRKPSUwCOmChMldrOkpuOG0uhHloD9Yj-6UznTM-7PajACIsSF2c1nX_BN7RyjyTTH3b23LvraeKB1Ixs112n7pq-dJ0mgI2CZQxnK_c7dQBwHYsmAvE1nZ4LN_Rrct4_f4YrigaAhNXkVGTHbaNN84rexGzHBWJZ2IXiVEYI-iVXj-qexDXdWMnOrlni76_1ZA'}

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