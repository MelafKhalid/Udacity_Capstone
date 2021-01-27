import os
from flask import (
    Flask,
    render_template,
    request,
    Response,
    flash,
    redirect,
    url_for,
    jsonify,
    abort)
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import setup_db, db, Movies, Actors
from auth import AuthError, requires_auth
import sys


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app)
    # Set up CORS. Allow '*' for origins.
    CORS(app, resources={'/': {'origins': '*'}})

    @app.after_request
    def after_request(response):
        response.headers.add(
            'Access-Control-Allow-Headers',
            'Content-Type,Authorization,true')
        response.headers.add(
            'Access-Control-Allow-Methods',
            'GET,PUT,POST,DELETE,OPTIONS')
        return response

    @app.route('/', methods=['GET'])
    def index():
        return "Hello World"

    @app.route('/actors')
    @requires_auth('get:actors')
    def get_actors(jwt):

        try:

            total_actors = Actors.query.all()

            actors = [actor.format() for actor in total_actors]

            return jsonify({
                'success': True,
                'actors': actors
            }), 200

        except BaseException:
            abort(404)

    @app.route('/movies')
    @requires_auth('get:movies')
    def get_movies(jwt):

        try:

            total_movies = Movies.query.all()

            movies = [movie.format() for movie in total_movies]

            return jsonify({
                'success': True,
                'movies': movies
            }), 200

        except BaseException:
            abort(404)

    @app.route("/actors", methods=['POST'])
    @requires_auth("post:actors")
    def post_actors(jwt):

        try:

            body = request.get_json()
            name = body.get('name')
            age = body.get('age')
            gender = body.get('gender')

            movie_id = body.get('movie_id') if 'movie_id' in body else movie_id = None

            actor = Actors(
                name=name,
                age=age,
                gender=gender,
                movie_id=movie_id)
            actor.insert()

            return jsonify({
                'success': True,
                'actors': [actor.format()]
            }), 200

        except BaseException:
            print(sys.exc_info())
            abort(422)

    @app.route("/movies", methods=['POST'])
    @requires_auth("post:movies")
    def post_movies(jwt):

        try:

            body = request.get_json()
            title = body.get('title')
            release_date = body.get('release_date')

            movie = Movies(title=title, release_date=release_date)
            movie.insert()

            return jsonify({
                'success': True,
                'movies': [movie.format()]
            }), 200

        except BaseException:
            abort(422)

    @app.route("/actors/<actor_id>", methods=['PATCH'])
    @requires_auth("patch:actors")
    def patch_actors(jwt, actor_id):

        actor = Actors.query.get(actor_id)

        if not actor:
            abort(404)

        try:
            body = request.get_json()

            if 'name' in body:
                actor.name = body.get('name')

            if 'age' in body:
                actor.age = body.get('age')

            if 'gender' in body:
                actor.gender = body.get('gender')

            if 'movie_id' in body:
                actor.movie_id = body.get('movie_id')

            actor.update()

            return jsonify({
                'success': True,
                'actors': [actor.format()]
            }), 200

        except BaseException:
            abort(422)

    @app.route("/movies/<movie_id>", methods=['PATCH'])
    @requires_auth("patch:movies")
    def patch_movies(jwt, movie_id):

        movie = Movies.query.get(movie_id)

        if not movie:
            abort(404)

        try:

            body = request.get_json()

            if 'title' in body:
                movie.title = body.get('title')

            if 'release_date' in body:
                movie.release_date = json.dumps(body.get('release_date'))

            movie.update()

            return jsonify({
                'success': True,
                'movies': [movie.format()]
            }), 200

        except BaseException:
            abort(422)

    @app.route('/actors/<actor_id>', methods=['DELETE'])
    @requires_auth('delete:actors')
    def delete_actors(jwt, actor_id):

        actor = Actors.query.get(actor_id)

        if not actor:
            abort(404)

        try:

            actor.delete()

            return jsonify({
                'success': True,
                'delete': actor_id
            }), 200

        except BaseException:
            abort(422)

    @app.route('/movies/<movie_id>', methods=['DELETE'])
    @requires_auth('delete:movies')
    def delete_movies(jwt, movie_id):

        movie = Movies.query.get(movie_id)

        if not movie:
            abort(404)

        try:

            movie.delete()

            return jsonify({
                'success': True,
                'delete': movie_id
            }), 200

        except BaseException:
            abort(422)

 # Error Handling.

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'success': False,
            'error': 400,
            'message': 'bad request'
        }), 400

    @app.errorhandler(401)
    def unauthorized(error):
        return jsonify({
            'success': False,
            'error': 401,
            'message': 'unauthorized '
        }), 401

    @app.errorhandler(403)
    def forbidden(error):
        return jsonify({
            'success': False,
            'error': 403,
            'message': 'forbidden'
        }), 403

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': 'resourse not found'
        }), 404

    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            'success': False,
            'error': 405,
            'message': 'method not allowed'
        }), 405

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
            'success': False,
            'error': 500,
            'message': 'internal server errors'
        }), 500

    @app.errorhandler(AuthError)
    def handle_auth_error(e):
        response = jsonify(e.error)
        response.status_code = e.status_code
        return response

    return app


app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
