# Coffee Shop Backend

## Getting Started

This is the Udacity Coffee Shop backend described in the main readme. 

Its purpose is to provide RBAC to the drinks menu.

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform
in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Environment

First, you have to setup a virtual environment for the project, to prevent
cluttering your Python system packages with this project packages.

```bash
cd [project_folder]
virtualenv venv
venv\Scripts\activate.bat
```

Instructions for setting up a virual enviornment for your platform can be 
found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies
by navigating to the `/backend` directory and running:

```bash
cd backend
pip install -r requirements.txt
```

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices
  framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) and 
  [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/) are 
  libraries to handle the lightweight sqlite database. Since we want you to 
  focus on auth, we handle the heavy lift for you in `./src/database/models.py`. 
  We recommend skimming this code first so you know how to interface with the Drink model.

- [jose](https://python-jose.readthedocs.io/en/latest/) JavaScript Object 
  Signing and Encryption for JWTs. Useful for encoding, decoding, and 
  verifying JWTS.

## Running the server

The `.flaskenv` file contains the environment variables needed to run flask.

There is **no need** for:
```
set FLASK_APP=src/api
set FLASK_ENV=development
```

From the `[project_folder]\backend` folder type the command:
```bash
flask run
```

## Tests

To unittest: 

- open the `test_api.py` file.
- set valid tokens for Barister and Manager roles `BARISTER_TOKEN` and `MANAGER_TOKEN`.
- save the file and:

```commandline
python test_api.py
```

You can test using postman. Import `udacity-fsnd-udaspicelatte.postman_collection.json`
file and run test. ___Don't forget to set valid tokens for Barister and Manager roles___.

## Tasks

The authentication system in this project is based upon third party 
authentication service to prevent all of the security issues known with 
passwords usage and/or storage.

Udacity Coffee Shop uses the [Auth0](https://auth0.com) as a third party
authentication and authorization service.

### Setup Auth0

1. Create a new Auth0 Account
2. Select a unique tenant domain
3. Create a new, single page web application
4. Create a new API
    - in API Settings:
        - Enable RBAC
        - Enable Add Permissions in the Access Token
5. Create new API permissions:
    - `get:drinks-detail`
    - `post:drinks`
    - `patch:drinks`
    - `delete:drinks`
6. Create new roles for:
    - Barista: can `get:drinks-detail`
    - Manager: can perform all actions

## API Reference

### Getting Started
- Base URL: At present this app can only be run locally and is not hosted as
  a base URL. The backend app is hosted at the default, `http://127.0.0.1:5000/`, 
  which is set as a proxy in the frontend configuration.

### Error Handling
Errors are returned as JSON objects in the following format:
```
{
    "success": False, 
    "error": 400,
    "message": "bad request"
}
```
The API will return three error types when requests fail:
- 400: bad request
- 401: unauthorized
- 403: access forbidden
- 404: resource not found
- 422: unprocessable

### Endpoints

####GET /drinks

##### General

- Returns a stripped list of the available drinks

##### Example

```json5
{
  "drinks": [
    {
      "id": 2,
      "recipe": [
        {
          "color": "green",
          "parts": 1
        },
        {
          "color": "yellow",
          "parts": 1
        }
      ],
      "title": "Drink 2"
    },
    {
      "id": 3,
      "recipe": [
        {
          "color": "pink",
          "parts": 1
        },
        {
          "color": "black",
          "parts": 1
        }
      ],
      "title": "Drink 3"
    },
    {
      "id": 4,
      "recipe": [
        {
          "color": "blue",
          "parts": 1
        }
      ],
      "title": "Water3"
    }
  ],
  "success": true
}
```

#### GET /drinks-detail

##### General

- Returns detailed composition of the drinks
- Needs: `get:drinks-detail` permission

##### Example

```commandline
curl "http://127.0.0.1:5000/drinks-detail" -H "Accept: application/json, text/plain, */*" -H "Origin: http://localhost:4200" -H "Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlNsV1ZCaFkwVzVfYTNseEZ1QldLWiJ9.eyJpc3MiOiJodHRwczovL21hbmlhbmlzLmV1LmF1dGgwLmNvbS8iLCJzdWIiOiJnb29nbGUtb2F1dGgyfDExNTk4Mzc0MTA1NjMyMzc3OTc0NCIsImF1ZCI6WyJ1ZGFjaXR5X2NvZmZlZV9zaG9wX2FwaSIsImh0dHBzOi8vbWFuaWFuaXMuZXUuYXV0aDAuY29tL3VzZXJpbmZvIl0sImlhdCI6MTU4NjY3Mzg2NiwiZXhwIjoxNTg2NzYwMjY1LCJhenAiOiJ4ckJiSzJ4TVlNNnRhS3pTUDFteTFzNTI2dDhucnlGYSIsInNjb3BlIjoib3BlbmlkIHByb2ZpbGUgZW1haWwiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6ZHJpbmtzIiwiZ2V0OmRyaW5rcy1kZXRhaWwiLCJwYXRjaDpkcmlua3MiLCJwb3N0OmRyaW5rcyJdfQ.ICfBJAiXl5AFS4sn91Orql5lVwjK5H6m1oVMTMFcQuAYc8n0Uxkd-pZ9Y-mFy25vj2JdDR4w2rqcvxh8Z32ry7bYjLfu5YSecsEFsB7o7DNtbs5zdOEfXY3dAlgmETHm20BVW1QBjyTy6VoWvNng3S5tl_VECUIGxHJPghxvjqOcxckBphUT1AvkXQHrB7BH2jDJT9QegCTmolZ1NBU-YYD2Y_PfTMJmYd7ooSKlssOSGeWQMaIZVunRvO38KKfE8z0I7KaZ1sM3mq8Kj_1jROiFfk6OdenIKMn01FR4hu1iKGp4Iz7sJrC2Tp7-GzkZ4EsHHCV_4v6KXjXQVIDE9g"
```

```json5
{
  "drinks": [
    {
      "id": 2,
      "recipe": [
        {
          "color": "green",
          "name": "Drink 2 - Part 1",
          "parts": 1
        },
        {
          "color": "yellow",
          "name": "Drink 2 - Part 2",
          "parts": 1
        }
      ],
      "title": "Drink 2"
    },
    {
      "id": 3,
      "recipe": [
        {
          "color": "pink",
          "name": "Drink 3 - Part 1",
          "parts": 1
        },
        {
          "color": "black",
          "name": "Drink 3 - Part 2",
          "parts": 1
        }
      ],
      "title": "Drink 3"
    },
    {
      "id": 4,
      "recipe": [
        {
          "color": "blue",
          "name": "Water",
          "parts": 1
        }
      ],
      "title": "Water3"
    }
  ],
  "success": true
}
```

#### POST /drinks

##### General

- Inserts a new drink
- Needs `post:drinks` permission

##### Example

```commandline
curl "http://127.0.0.1:5000/drinks" -H "Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlNsV1ZCaFkwVzVfYTNseEZ1QldLWiJ9.eyJpc3MiOiJodHRwczovL21hbmlhbmlzLmV1LmF1dGgwLmNvbS8iLCJzdWIiOiJnb29nbGUtb2F1dGgyfDExNTk4Mzc0MTA1NjMyMzc3OTc0NCIsImF1ZCI6WyJ1ZGFjaXR5X2NvZmZlZV9zaG9wX2FwaSIsImh0dHBzOi8vbWFuaWFuaXMuZXUuYXV0aDAuY29tL3VzZXJpbmZvIl0sImlhdCI6MTU4NjY3Mzg2NiwiZXhwIjoxNTg2NzYwMjY1LCJhenAiOiJ4ckJiSzJ4TVlNNnRhS3pTUDFteTFzNTI2dDhucnlGYSIsInNjb3BlIjoib3BlbmlkIHByb2ZpbGUgZW1haWwiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6ZHJpbmtzIiwiZ2V0OmRyaW5rcy1kZXRhaWwiLCJwYXRjaDpkcmlua3MiLCJwb3N0OmRyaW5rcyJdfQ.ICfBJAiXl5AFS4sn91Orql5lVwjK5H6m1oVMTMFcQuAYc8n0Uxkd-pZ9Y-mFy25vj2JdDR4w2rqcvxh8Z32ry7bYjLfu5YSecsEFsB7o7DNtbs5zdOEfXY3dAlgmETHm20BVW1QBjyTy6VoWvNng3S5tl_VECUIGxHJPghxvjqOcxckBphUT1AvkXQHrB7BH2jDJT9QegCTmolZ1NBU-YYD2Y_PfTMJmYd7ooSKlssOSGeWQMaIZVunRvO38KKfE8z0I7KaZ1sM3mq8Kj_1jROiFfk6OdenIKMn01FR4hu1iKGp4Iz7sJrC2Tp7-GzkZ4EsHHCV_4v6KXjXQVIDE9g" -H "Content-Type: application/json" --data-binary "{\"id\":-1,\"title\":\"Milked Coffee 2\",\"recipe\":[{\"name\":\"Milk\",\"color\":\"lightgray\",\"parts\":2},{\"name\":\"Coffee\",\"color\":\"black\",\"parts\":1}]}"
```

```json5
{
  "drinks": [
    {
      "id": 6,
      "recipe": [
        {
          "color": "lightgray",
          "name": "Milk",
          "parts": 2
        },
        {
          "color": "black",
          "name": "Coffee",
          "parts": 1
        }
      ],
      "title": "Milked Coffee 2"
    }
  ],
  "success": true
}
```

#### PATCH /drinks/<id>

##### General 

- Updates the drink with the <id> identifier.
- Needs `patch:drinks` permission

##### Example

```commandline
curl "http://127.0.0.1:5000/drinks/6" -X PATCH -H "Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlNsV1ZCaFkwVzVfYTNseEZ1QldLWiJ9.eyJpc3MiOiJodHRwczovL21hbmlhbmlzLmV1LmF1dGgwLmNvbS8iLCJzdWIiOiJnb29nbGUtb2F1dGgyfDExNTk4Mzc0MTA1NjMyMzc3OTc0NCIsImF1ZCI6WyJ1ZGFjaXR5X2NvZmZlZV9zaG9wX2FwaSIsImh0dHBzOi8vbWFuaWFuaXMuZXUuYXV0aDAuY29tL3VzZXJpbmZvIl0sImlhdCI6MTU4NjY3Mzg2NiwiZXhwIjoxNTg2NzYwMjY1LCJhenAiOiJ4ckJiSzJ4TVlNNnRhS3pTUDFteTFzNTI2dDhucnlGYSIsInNjb3BlIjoib3BlbmlkIHByb2ZpbGUgZW1haWwiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6ZHJpbmtzIiwiZ2V0OmRyaW5rcy1kZXRhaWwiLCJwYXRjaDpkcmlua3MiLCJwb3N0OmRyaW5rcyJdfQ.ICfBJAiXl5AFS4sn91Orql5lVwjK5H6m1oVMTMFcQuAYc8n0Uxkd-pZ9Y-mFy25vj2JdDR4w2rqcvxh8Z32ry7bYjLfu5YSecsEFsB7o7DNtbs5zdOEfXY3dAlgmETHm20BVW1QBjyTy6VoWvNng3S5tl_VECUIGxHJPghxvjqOcxckBphUT1AvkXQHrB7BH2jDJT9QegCTmolZ1NBU-YYD2Y_PfTMJmYd7ooSKlssOSGeWQMaIZVunRvO38KKfE8z0I7KaZ1sM3mq8Kj_1jROiFfk6OdenIKMn01FR4hu1iKGp4Iz7sJrC2Tp7-GzkZ4EsHHCV_4v6KXjXQVIDE9g" -H "Content-Type: application/json" --data-binary "{\"id\":6,\"recipe\":[{\"color\":\"lightgray\",\"name\":\"Milk\",\"parts\":2},{\"name\":\"Chocolate\",\"color\":\"chocolate\",\"parts\":1},{\"color\":\"black\",\"name\":\"Coffee\",\"parts\":1}],\"title\":\"Milked Coffee 2\"}"
```

```json5
{
  "drinks": [
    {
      "id": 6,
      "recipe": [
        {
          "color": "lightgray",
          "name": "Milk",
          "parts": 2
        },
        {
          "color": "chocolate",
          "name": "Chocolate",
          "parts": 1
        },
        {
          "color": "black",
          "name": "Coffee",
          "parts": 1
        }
      ],
      "title": "Milked Coffee 2"
    }
  ],
  "success": true
}
```

#### DELETE /drinks/<id>

#### General

- Deletes one drink knowing its <id>
- Needs `delete:drinks` permission

#### Example

```commandline
curl "http://127.0.0.1:5000/drinks/6" -X DELETE -H "Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlNsV1ZCaFkwVzVfYTNseEZ1QldLWiJ9.eyJpc3MiOiJodHRwczovL21hbmlhbmlzLmV1LmF1dGgwLmNvbS8iLCJzdWIiOiJnb29nbGUtb2F1dGgyfDExNTk4Mzc0MTA1NjMyMzc3OTc0NCIsImF1ZCI6WyJ1ZGFjaXR5X2NvZmZlZV9zaG9wX2FwaSIsImh0dHBzOi8vbWFuaWFuaXMuZXUuYXV0aDAuY29tL3VzZXJpbmZvIl0sImlhdCI6MTU4NjY3Mzg2NiwiZXhwIjoxNTg2NzYwMjY1LCJhenAiOiJ4ckJiSzJ4TVlNNnRhS3pTUDFteTFzNTI2dDhucnlGYSIsInNjb3BlIjoib3BlbmlkIHByb2ZpbGUgZW1haWwiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6ZHJpbmtzIiwiZ2V0OmRyaW5rcy1kZXRhaWwiLCJwYXRjaDpkcmlua3MiLCJwb3N0OmRyaW5rcyJdfQ.ICfBJAiXl5AFS4sn91Orql5lVwjK5H6m1oVMTMFcQuAYc8n0Uxkd-pZ9Y-mFy25vj2JdDR4w2rqcvxh8Z32ry7bYjLfu5YSecsEFsB7o7DNtbs5zdOEfXY3dAlgmETHm20BVW1QBjyTy6VoWvNng3S5tl_VECUIGxHJPghxvjqOcxckBphUT1AvkXQHrB7BH2jDJT9QegCTmolZ1NBU-YYD2Y_PfTMJmYd7ooSKlssOSGeWQMaIZVunRvO38KKfE8z0I7KaZ1sM3mq8Kj_1jROiFfk6OdenIKMn01FR4hu1iKGp4Iz7sJrC2Tp7-GzkZ4EsHHCV_4v6KXjXQVIDE9g"
```

```json5
{
  "delete": 6,
  "success": true
}
```

## Authors

- Initiated by **Udacity Coaches**
- API/Tests and Documentation by **Mohamed Anis MANI**

## Acknowledgments

To the Udacity coaches.