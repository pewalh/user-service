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
4. First time - Set up a clean local database:
    ```
    poetry run prisma db push
    ```
    Note: The database storage file *not* included in git.


## Run the service
Run the service within the virtual environment with 
```
poetry run uvicorn user-service:app --host 0.0.0.0 --port 8000
```
This starts the service locally. It will use a local sqlite database in ***TODO*** 

Follow the link `link` to interact with the service via its swagger ui/doc.


## API
***TODO*** 


## Tests
***TODO***

