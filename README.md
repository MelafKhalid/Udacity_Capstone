# Casting Agency Full Stack Nanodegree

The Casting Agency models a company that is responsible for creating movies and managing and assigning actors to those movies.

## Motivation

This project contains all knowledge that I learned during Full Stack Development Nanodegree

- I am in the Information Technology industry where all the tools will help me do my job efficiently

- I developed this project to make use of all the knowledge I acquired in this nanodegree and hence gain confidence in all these skills.

- I wanted to contribute to developing the open-source community by building applications

- 

Completing this app gave me the essential skills and enthusiasm to continue learning and development in the field of software programming

## Getting Started

Application hosted on Heroku: https://boiling-mountain-94717.herokuapp.com/

## Development Setup

### Python 3.8

Follow instructions to install the latest version of python for your platform in the python docs

### Install the dependencies

```
pip3 install -r requirements.txt
```

### Export Environment Variables

Refer to the ```setup.sh``` file and export the environment variables for the project.

### Install new packages in the file

```
pip install flask_script
pip install flask_migrate
pip install psycopg2-binary
```

### Run Database Migrations

```
python manage.py db init
python manage.py db migrate
python manage.py db upgrade
```

### Run the development server

```
export FLASK_APP=app.py
export FLASK_ENV=development
flask run
```
Setting the FLASK_ENV variable to development will detect file changes and restart the server automatically. Setting the FLASK_APP variable to app.py directs flask to run app.py and run the application.



## Error Handling

Errors are returned as JSON in the following format:

```
{
    "success": False,
    "error": 404,
    "message": "resource not found"
}
```
The API will return three types of errors:

- 404 – resource not found
- 422 – unprocessable
- 401 - Unauthorized
- 400 - bad request
- 500 - internal server error
- 403 - Forbidden

## API Documentation

- Base URL For App: https://boiling-mountain-94717.herokuapp.com

- Authentication: Auth0

- Get a new token: <html> <a href="https://fsnd-melaf.us.auth0.com/login?state=g6Fo2SBDaGtwNFNfYktfZVRuaDI0M21rWW1GMDdweFBjaXRkaKN0aWTZIHNRUWVhaTBNV2U0OHFucGEtLXR4cmdkTzAwckZnemlvo2NpZNkgeTFLekxub2tBTDdvZFlHM0pzRlE2VWVGclI1QThSc1Q&client=y1KzLnokAL7odYG3JsFQ6UeFrR5A8RsT&protocol=oauth2&audience=Capstone&response_type=token&redirect_uri=https%3A%2F%2Flocalhost%3A8080%2Flogin-results"> Click Here </a></html>

### Roles:

### Casting Assistant

Can view actors and movies

- get:actors

- get:movies

email: casting.assistant@gmail.com 

password: Assistant123

### Casting Director

All permissions a Casting Assistant has and

Add or delete an actor from the database

- post:actors

- delete:actors

Modify actors or movies

- patch:actors

- patch:movies

email: Casting.Director@gmail.com

password: Director@123

### Executive Producer

All permissions a Casting Director has and

Add or delete a movie from the database

- post:movies

- delete:movies

email: Executive.Producer@gmail.com

password: Executive@123

## Endpoints

To test the endpoints you need to replace tokens by the actual value of valid tokens in all these curl requests.

### GET /actors

- General: Return all actors in from the Database

- Sample: curl -H "Authorization: bearer Assisant_jwt" https://boiling-mountain-94717.herokuapp.com/actors

```
{
    "actors": [
        {
            "age":15,
            "gender":"male",
            "id":2,
            "movie_id":null,
            "name":"mohammad"
    },
    {
            "age":15,
            "gender":"male",
            "id":3,
            "movie_id":null,
            "name":"mohammad"
        }
        ],
            "success":true
}
```

### GET /movies

- General: Return all movies in from the Database

- Sample: curl -H "Authorization: bearer Assisant_jwt" https://boiling-mountain-94717.herokuapp.com/movies

```
{
    "movies": [
        {
            "id":2,
            "release_date":"Mon, 10 Oct 2016 00:00:00 GMT",
            "title":"The Mud"
        }
            ],
            "success":true
}
```
### POST /actors

- General: Add a new actor to the database

- Sample: curl https://boiling-mountain-94717.herokuapp.com/actors -X POST -H "Authorization: bearer Director_Token" -H "Content-Type: application/json" -d '{"name": "Sara", "age":"18", "gender":"female"}'

```
{
    "actors": [
        {
            "age":18,
            "gender":"female",
            "id":4,
            "movie_id":null,
            "name":"Sara"
        }
            ],
            "success":true
}
```

### POST /movies

- General: Add a new movie to the database

- Sample: curl https://boiling-mountain-94717.herokuapp.com/movies -X POST -H "Authorization: bearer Executive_Token" -H "Content-Type: application/json" -d '{"title": "The Departed", "release_date":"2006-06-01"}'

```
{
    "movies": [
        {
            "id":3,
            "release_date":"Thu, 01 Jun 2006 00:00:00 GMT",
            "title":"The Departed"
        }
            ],
            "success":true
}
```

### PATCH /actors/<actor_id>

- General: Edit some information for actor

- Sample: curl -X PATCH https://boiling-mountain-94717.herokuapp.com/actors/2 --data '{"movie_id": "3"}' -H "content-type: application/json" -H "Authorization: bearer Director_Token"

```
{
    "actors": [
        {
            "age":15,
            "gender":"male",
            "id":2,
            "movie_id":3,
            "name":"mohammad"
        }
            ],
            "success":true
}
```

### PATCH '/movies/<movie_id>'

- General: Edit some information for movie

- Sample: curl -X PATCH https://boiling-mountain-94717.herokuapp.com/movies/3 --data '{"title": "Parasite"}' -H "content-type: application/json" -H "Authorization: bearer Director_Token"

```
{
     "movies": [
        {
             "id":3,
             "release_date":"Thu, 01 Jun 2006 00:00:00 GMT",
             "title":"Parasite"
        }
             ],
             "success":true
}
```

### DELETE /actors/<actor_id>

- General: Delete an actor from the database

- Sample: curl -X DELETE https://boiling-mountain-94717.herokuapp.com/actors/3 -H "Authorization: bearer Executive_Token"

```
{
    "delete":"3",
    "success":true
}
```

### DELETE /movies/<movie_id>

- General: Delete an movie from the database

- Sample: curl -X DELETEhttps://boiling-mountain-94717.herokuapp.com/movies/3 -H "Authorization: bearer Executive_Token"


```
{
    "delete":"3",
    "success":true
}
```

## Testing

To run the tests, run

```
dropdb capstone
createdb capstone
python test_app.py
```

## Postman

Postman to test all API Provided