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
This starts the service locally. It will use a local sqlite database in ***TODO*** 

A Swagger UI for documentation and testing of/interaction with the API is available in [http://localhost:8000/doc](http://localhost:8000/docs).


## API
***TODO*** 


## Tests
***TODO***



# TODO for more extensive service
* Change database to postgresql for better scaling and concurrent writes etc
* wrap the service in a docker container
* Implement separate endpoints for CRUD:ing the contact details table. Now everything goes through user, which is ok for now but may entangle concerns
