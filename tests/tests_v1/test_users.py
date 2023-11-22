import pytest
from prisma import Prisma
from main import app
from fastapi.testclient import TestClient 
from fastapi import HTTPException, Depends
from prisma.models import User, ContactDetails
from unittest.mock import patch, Mock
from user_service.prisma.database import get_db
from user_service.api.v1.models import UserBasicInfo, UserInfo, UserInfoFull, ContactDetailsData




client = TestClient(app)






# --------- GET METHODS ---------
# get all users with pagination, no relational data
def test_get_users(fastapi_dep):

    class MockUser():
        async def find_many(self, skip: int = 0, take: int = 100):
            return [
                User(id=1, username="user0", email="email0", active=True),
                User(id=2, username="user1", email="email1", active=True),
                User(id=3, username="user2", email="email2", active=True),
            ]
    class MockPrisma():
        user = MockUser()
    def _get_db():
        return MockPrisma()


    # patch the db dependency get_db
    with fastapi_dep(app).override({get_db: _get_db}):
        response = client.get("/api/v1/users/")
        assert response.status_code == 200
        assert response.json() == [
            {"id": 1, "username": "user0", "email": "email0", "active": True},
            {"id": 2, "username": "user1", "email": "email1", "active": True},
            {"id": 3, "username": "user2", "email": "email2", "active": True},
        ]

        

# get a single user by specifying the user id
def test_get_user(fastapi_dep):

    class MockUser():
        async def find_unique(self, where: dict, include: dict):
            return User(id=1, username="user0", email="email0", active=True, contactDetails=None)
    class MockPrisma():
        user = MockUser()
    def _get_db():
        return MockPrisma()


    # patch the db dependency get_db
    with fastapi_dep(app).override({get_db: _get_db}):
        response = client.get("/api/v1/users/1")
        assert response.status_code == 200
        assert response.json() == {
            "id": 1, "username": "user0", "email": "email0", "active": True, "contactDetails": None
        }

# negative test for get_user
def test_get_user_not_found(fastapi_dep):

    class MockUser():
        async def find_unique(self, where: dict, include: dict):
            return None
    class MockPrisma():
        user = MockUser()
    def _get_db():
        return MockPrisma()


    # patch the db dependency get_db
    with fastapi_dep(app).override({get_db: _get_db}):
        response = client.get("/api/v1/users/1")
        assert response.status_code == 404
        assert response.json() == {
            "detail": "User with id '1' not found"
        }



# get a single user by specifying the email
def test_get_user_by_email(fastapi_dep):

    class MockUser():
        async def find_unique(self, where: dict, include: dict):
            return User(id=1, username="user0", email="email0", active=True, contactDetails=None)
    class MockPrisma():
        user = MockUser()
    def _get_db():
        return MockPrisma()


    # patch the db dependency get_db
    with fastapi_dep(app).override({get_db: _get_db}):
        response = client.get("/api/v1/users/email/email0")
        assert response.status_code == 200
        assert response.json() == {
            "id": 1, "username": "user0", "email": "email0", "active": True, "contactDetails": None
        }


# negative test for get_user_by_email
def test_get_user_by_email_not_found(fastapi_dep):

    class MockUser():
        async def find_unique(self, where: dict, include: dict):
            return None
    class MockPrisma():
        user = MockUser()
    def _get_db():
        return MockPrisma()


    # patch the db dependency get_db
    with fastapi_dep(app).override({get_db: _get_db}):
        response = client.get("/api/v1/users/email/email0")
        assert response.status_code == 404
        assert response.json() == {
            "detail": "User with email 'email0' not found"
        }


# --------- CREATE METHODS ---------

# create a new user
def test_create_user(fastapi_dep):

    class MockUser():
        async def create(self, data: dict):
            return User(id=1, username=data["username"], email=data["email"], active=True, contactDetails=None)
    class MockPrisma():
        user = MockUser()
    def _get_db():
        return MockPrisma()


    # patch the db dependency get_db
    with fastapi_dep(app).override({get_db: _get_db}):
        response = client.post("/api/v1/users/", json={
            "username": "user35",
            "email": "email35",
        })
        assert response.status_code == 200
        assert response.json() == {
            "id": 1, "username": "user35", "email": "email35", "active": True, "contactDetails": None
        }


# --------- UPDATE METHODS ----------
# update a users username, by specifying the user id
def test_update_user_username(fastapi_dep):
    class MockUser():
        async def update(self, where: dict, data: dict, include: dict):
            return User(id=where["id"], username=data["username"], email="email0", active=True, contactDetails=None)
    class MockPrisma():
        user = MockUser()
    def _get_db():
        return MockPrisma()

    # patch the db dependency get_db
    with fastapi_dep(app).override({get_db: _get_db}):
        response = client.put("/api/v1/users/1/username", params={
            "username": "user35",
        })
        assert response.status_code == 200
        assert response.json() == {
            "id": 1, "username": "user35", "email": "email0", "active": True, "contactDetails": None
        }

# update a users email
def test_update_user_email(fastapi_dep):
    class MockUser():
        async def update(self, where: dict, data: dict, include: dict):
            return User(id=where["id"], username="user0", email=data["email"], active=True, contactDetails=None)
    class MockPrisma():
        user = MockUser()
    def _get_db():
        return MockPrisma()

    # patch the db dependency get_db
    with fastapi_dep(app).override({get_db: _get_db}):
        response = client.put("/api/v1/users/1/email", params={
            "email": "email35",
        })
        assert response.status_code == 200
        assert response.json() == {
            "id": 1, "username": "user0", "email": "email35", "active": True, "contactDetails": None
        }

# update a users active status
def test_update_user_active(fastapi_dep):
    class MockUser():
        async def update(self, where: dict, data: dict, include: dict):
            return User(id=where["id"], username="user0", email="email0", active=data["active"], contactDetails=None)
    class MockPrisma():
        user = MockUser()
    def _get_db():
        return MockPrisma()

    # patch the db dependency get_db
    with fastapi_dep(app).override({get_db: _get_db}):
        response = client.put("/api/v1/users/1/active", params={
            "active": False,
        })
        assert response.status_code == 200
        assert response.json() == {
            "id": 1, "username": "user0", "email": "email0", "active": False, "contactDetails": None
        }

# update a users contact details
def test_update_user_contact_details(fastapi_dep):
    
    
    class MockContact():
        async def upsert(self, where: dict, data: dict):
            contact_details = ContactDetails(id=1, address=data["create"]["address"], phoneNumber=data["create"]["phoneNumber"], userId=where["userId"])
            user = User(id=where["userId"], username="user0", email="email0", active=True, contactDetails=contact_details)
            contact_details.user = user
            return contact_details
    class MockUser():
        async def find_unique(self, where: dict, include: dict):
            contact_details = ContactDetails(id=1, address="address35", phoneNumber="phoneNumber35", userId=where["id"])
            return User(id=where["id"], username="user0", email="email0", active=True, contactDetails=contact_details)
        
    class MockPrisma():
        contactdetails = MockContact()
        user = MockUser()
    def _get_db():
        return MockPrisma()

    # patch the db dependency get_db
    with fastapi_dep(app).override({get_db: _get_db}):
        response = client.put("/api/v1/users/1/contact_details", json={
            "address": "address35",
            "phoneNumber": "phoneNumber35",
        })
        assert response.status_code == 200
        assert response.json() == {
            "id": 1, "username": "user0", "email": "email0", "active": True, "contactDetails": {
                "address": "address35", "phoneNumber": "phoneNumber35"
            }
        }


# --------- DELETE METHODS ----------
# delete a user by specifying the user id
def test_delete_user(fastapi_dep):
    class MockUser():
        async def delete(self, where: dict):
            return User(id=where["id"], username="user0", email="email0", active=True, contactDetails=
                        ContactDetails(id=1, address="address0", phoneNumber="phoneNumber0", userId=where["id"]))            
    class MockPrisma():
        user = MockUser()
    def _get_db():
        return MockPrisma()

    # patch the db dependency get_db
    with fastapi_dep(app).override({get_db: _get_db}):
        response = client.delete("/api/v1/users/1")
        assert response.status_code == 200
        assert response.json() == {
            "id": 1, "username": "user0", "email": "email0", "active": True, "contactDetails": {
                "address": "address0", "phoneNumber": "phoneNumber0"
            }
        }

# negative test for delete_user
def test_delete_user_not_found(fastapi_dep):
    class MockUser():
        async def delete(self, where: dict):
            return None
    class MockPrisma():
        user = MockUser()
    def _get_db():
        return MockPrisma()

    # patch the db dependency get_db
    with fastapi_dep(app).override({get_db: _get_db}):
        response = client.delete("/api/v1/users/1")
        assert response.status_code == 404
        assert response.json() == {
            "detail": "User with id '1' not found"
        }

# delete a users contact details, by specifying the user id

def test_delete_user_contact_details(fastapi_dep):
    class MockContact():
        async def delete(self, where: dict):
            return ContactDetails(id=where["userId"], address="address0", phoneNumber="phoneNumber0", userId=where["userId"])
    class MockPrisma():
        contactdetails = MockContact()
    def _get_db():
        return MockPrisma()

    # patch the db dependency get_db
    with fastapi_dep(app).override({get_db: _get_db}):
        response = client.delete("/api/v1/users/1/contact_details")
        assert response.status_code == 200
        assert response.json() == {
            "address": "address0", "phoneNumber": "phoneNumber0"
        }
    
# negative test for delete_user_contact_details
def test_delete_user_contact_details_not_found(fastapi_dep):
    class MockContact():
        async def delete(self, where: dict):
            return None
    class MockPrisma():
        contactdetails = MockContact()
    def _get_db():
        return MockPrisma()

    # patch the db dependency get_db
    with fastapi_dep(app).override({get_db: _get_db}):
        response = client.delete("/api/v1/users/1/contact_details")
        assert response.status_code == 404
        assert response.json() == {
            "detail": "Contact details for user with id '1' not found"
        }

