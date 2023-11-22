# user-service
Simple microservice that demos user data handling.

The service uses **FastAPI** on **uvicorn** for the api and, for simplicity, a **sqlite** database interfaced with **Prisma** ORM.
For "real" use, wrap the service in a docker container and use another database like e.g. a PostgreSQL db. 


**Poetry** is used for package and virtual environment management.


## Setup
1. Install [python 3.12](https://www.python.org/downloads/)
2. Install poetry:
    ```
    pip install poetry
    ```
3. `cd <project dir>` then:
    ```
    poetry install
    ```
    to create the virtual environment and install the project dependecies.
4. Create or update the database:
    ```
    poetry run prisma db push
    ```
    Note: The database storage file *not* included in git.
    
5. Generate the prisma client: 
    ```
    poetry run prisma generate
    ```


## Run the service
Run the service within the virtual environment with 
```
poetry run uvicorn main:app --port 8000
```
This starts the service locally. It will use a local sqlite database in the file `database.db` placed in the project directory.

A Swagger UI for documentation and testing of/interaction with the API is available in [http://localhost:8000/doc](http://localhost:8000/docs).


## API
Only ***users*** api has been implemented even if the contact details lives in a separate table. The approach is rather more functional than pure CRUD.
As for now the contact details primary key is never exposed through the API since that is not relevant information when interacting with the user. A contact detail record can be created, updated and deleted via the user api.

Endpoints:
* Get all users: `GET /api/v1/users`: Gets all users with performance in mind, implementing pagination and no loading of relational dependencies (the contact details). Returns empty list if no users are found.
* Get full user info by `user_id` or `email`, `GET /api/v1/users/{user_id}` resp `GET /api/v1/users/email/{email}`. Returns 404 error if id is not recognized. Loads full info with contact details into response.
* Create user: `POST /api/v1/users`: Create a user by specifying email and username.
Returns full info into response.
* Update username: `PUT /api/v1/users/{user_id}/username`: Updates username if user_id is found, else returns 404.
* Update email: `PUT /api/v1/users/{user_id}/email`: Updates email if user_id is found, else returns 404.
* Update active status: `PUT /api/v1/users/{user_id}/active`: Updates active flag if user_id is found, else returns 404.
* Update active status: `PUT /api/v1/users/{user_id}/contact_details`: Creates or updates contact details for the user if user_id is found, else returns 404.
* Delete user: `DELETE /api/v1/users/{user_id}`: Delete the user and returns which user was deleted if user_id is found, else returns 404. Will delete any associated contact details records aswell.
* Delete contact details record: `DELETE /api/v1/users/{user_id}/contact_details`: Delete the contact details associated with the user_id if user_id is found and returns contact details, else returns 404.




## Tests
Type checking is performed with mypy. Run with:
```
poetry run mypy
```
There are some relational includes that it cannot understand. Lines like `include={"contactDetails": True})` where ` # type: ignore[prisma-parsing]` has been added to suppress warnings.


Unit tests can be run with:
```
poetry run pytest
```
These tests mock the database and tests more or less only shallowly the api.




## TODO for more extensive implementation
* Change database to postgresql for better scaling and concurrent writes etc
* wrap the service in a docker container
* Implement separate endpoints for CRUD:ing the contact details table. Now everything goes through user, which is ok for now but may entangle concerns
* Investigate if there is another way to load the relational dependencies in a way mypy can understand so that no warning suppressions are needed.
* Add system tests that tests the db interface.

