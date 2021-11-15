## imdb extract

#### installation
To install the dependencies.
```bash
$ pip install -r requirements.txt
```

#### database configuration
The database connection can be configured through `config.py` (environment specific). Examples of the URI that should be used for the connection are:

```python
SQLALCHEMY_DATABASE_URI = 'sqlite:///test.sqlite3'
SQLALCHEMY_DATABASE_URI = 'mysql://username:password@server/db'
```
#### database setup
To initially setup the database with pre-loaded movies and users.

```bash 
$ python setup.py
```
#### Authorization mechanism
Permissions are defined for the API access. For example, to add a movie, the POST API `/api/v1/movie` needs permission `CREATE_MOVIE`.

Role based access - The users are assigned the roles and permissions are assigned to the roles. 

This way when a new user is assigned an existing role through the API `/api/v1/user/<user id>/assign_role/<role id>` the permissions get attached to the new user.

```python
@movie.route('/api/v1/movie', methods=["POST"]) 
@token_required(['CREATE_MOVIE'])
def add_movie():
    ...

```



#### Authentication
API callout to the `/api/v1/auth` with username and password. This will generate a `token` which has to passed in the authentication token bearer with subsequent API calls.
The token generated from the `auth` API is valid for 4 hours.

Structure of the token:
```json 
{
    "email": "a@xyz.com",
    "first_name": "A",
    "last_name": "X",
    "permissions": [
        "CREATE_MOVIE",
        ...
        ],
    "roles": [
        "admin",
        ...
        ],
    "exp": "4 hours",
}
``` 

