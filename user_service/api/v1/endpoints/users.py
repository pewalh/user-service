from fastapi import APIRouter, Depends
from prisma import Prisma
from prisma.models import User
from prisma.partials import UserInfo, UserCreate, ContactDetailsData
from user_service.prisma.database import get_db


router = APIRouter(tags=["users"])


# --------- GET METHODS ---------

# get all users with pagination
@router.get("/users/", response_model=list[UserInfo])
async def get_users(offset:int = 0, limit:int = 100, db: Prisma = Depends(get_db)):
    users = await db.user.find_many(skip=offset, take=limit)
    return users

# get a single user by specifying the user id
@router.get("/users/{user_id}", response_model=UserInfo)
async def get_user(user_id: int, db: Prisma = Depends(get_db)):
    user = await db.user.find_unique(where={"id": user_id})
    return user

# get a single user by specifying the email
@router.get("/users/email/{email}", response_model=UserInfo)
async def get_user_by_email(email: str, db: Prisma = Depends(get_db)):
    user = await db.user.find_unique(where={"email": email})
    return user


# --------- CREATE METHODS ---------

# create a new user
@router.post("/users/", response_model=UserInfo)
async def create_user(user: UserCreate, db: Prisma = Depends(get_db)):
    user = await db.user.create(data=user.model_dump())
    return user


# ---------- UPDATE METHODS ----------

# update a users username, by specifying the user id
@router.put("/users/{user_id}/username", response_model=UserInfo)
async def update_user_username(user_id: int, username: str, db: Prisma = Depends(get_db)):
    user = await db.user.update(
        where={"id": user_id},
        data={"username": username},
    )
    return user


# update a users email
@router.put("/users/{user_id}/email", response_model=UserInfo)
async def update_user_email(user_id: int, email: str, db: Prisma = Depends(get_db)):
    user = await db.user.update(
        where={"id": user_id},
        data={"email": email},
    )
    return user


# update a users active status
@router.put("/users/{user_id}/active", response_model=UserInfo)
async def update_user_active(user_id: int, active: bool, db: Prisma = Depends(get_db)):
    user = await db.user.update(
        where={"id": user_id},
        data={"active": active},
    )
    return user


# update a users contact details, by specifying the user id
@router.put("/users/{user_id}/contact_details", response_model=UserInfo)
async def update_user_contact_details(user_id: int, contact_details: ContactDetailsData, db: Prisma = Depends(get_db)):
    # get the users contact details id if it exists
    user = await db.user.find_unique(where={"id": user_id})
    
    # contact_details_id is found by querying the contact details table for the user id
    contact_details = await db.contactdetails.find_unique(where={"userId": user_id})
    
    if contact_details is None:
        # create a new contact details entry
        contact_details = await db.contactdetails.create(data=contact_details.model_dump())
    else:
        # update the existing contact details entry
        contact_details = await db.contactdetails.update(
            where={"id": contact_details.id},
            data=contact_details.model_dump(),
        )
    # get the updated user (again to get the updated contact details right from db)
    user = await db.user.find_unique(where={"id": user_id})
    return user



# ---------- DELETE METHODS ----------

# delete a user, by specifying the user id
@router.delete("/users/{user_id}")
async def delete_user(user_id: int, db: Prisma = Depends(get_db)):
    await db.user.delete(where={"id": user_id})
    return {"message": "User deleted successfully."}

