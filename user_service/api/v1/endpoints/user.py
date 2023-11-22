from fastapi import APIRouter, Depends, HTTPException
from prisma import Prisma
from typing import Optional
from prisma.models import User
from user_service.api.v1.models import UserBasicInfo, UserInfo, UserInfoFull, ContactDetailsData
from user_service.prisma.database import get_db


router = APIRouter(tags=["users"])


def _return_full_user_or_raise(user_id:int, user: Optional[User]) -> UserInfoFull:
    if user is not None:
        return UserInfoFull(**user.model_dump())
    else:
        raise HTTPException(status_code=404, detail=f"User with id '{user_id}' not found")



# --------- GET METHODS ---------

# get all users with pagination, no relational data
@router.get("/users/", response_model=list[UserInfo])
async def get_users(offset:int = 0, limit:int = 100, db: Prisma = Depends(get_db)) -> list[UserInfo]:
    users = await db.user.find_many(skip=offset, take=limit)
    return [UserInfo(**user.model_dump()) for user in users]

# get a single user by specifying the user id
@router.get("/users/{user_id}", response_model=UserInfoFull)
async def get_user(user_id: int, db: Prisma = Depends(get_db)) -> UserInfoFull:
    user = await db.user.find_unique(
        where={"id": user_id}, 
        include={"contactDetails": True})  # type: ignore[prisma-parsing]
    return _return_full_user_or_raise(user_id, user)


# get a single user by specifying the email
@router.get("/users/email/{email}", response_model=UserInfoFull)
async def get_user_by_email(email: str, db: Prisma = Depends(get_db)) -> UserInfoFull:
    user = await db.user.find_unique(
        where={"email": email}, 
        include={"contactDetails": True})  # type: ignore[prisma-parsing]
    if user:
        return UserInfoFull(**user.model_dump())
    else:
        raise HTTPException(status_code=404, detail=f"User with email '{email}' not found")


# --------- CREATE METHODS ---------

# create a new user
@router.post("/users/", response_model=UserInfoFull)
async def create_user(user_info: UserBasicInfo, db: Prisma = Depends(get_db)) -> UserInfoFull:
    user = await db.user.create(
        data={
            "username": user_info.username,
            "email": user_info.email,
        },
    )
    return UserInfoFull(**user.model_dump())


# ---------- UPDATE METHODS ----------

# update a users username, by specifying the user id
@router.put("/users/{user_id}/username", response_model=UserInfoFull)
async def update_user_username(user_id: int, username: str, db: Prisma = Depends(get_db)) -> UserInfoFull:
    user = await db.user.update(
        where={"id": user_id},
        data={"username": username},
        include={"contactDetails": True},  # type: ignore[prisma-parsing]
    )
    return _return_full_user_or_raise(user_id, user)


# update a users email
@router.put("/users/{user_id}/email", response_model=UserInfoFull)
async def update_user_email(user_id: int, email: str, db: Prisma = Depends(get_db)) -> UserInfoFull:
    user = await db.user.update(
        where={"id": user_id},
        data={"email": email},
        include={"contactDetails": True}, # type: ignore[prisma-parsing]  
    )
    return _return_full_user_or_raise(user_id, user)


# update a users active status
@router.put("/users/{user_id}/active", response_model=UserInfoFull)
async def update_user_active(user_id: int, active: bool, db: Prisma = Depends(get_db)) -> UserInfoFull:
    user = await db.user.update(
        where={"id": user_id},
        data={"active": active},
        include={"contactDetails": True}, # type: ignore[prisma-parsing]
    )
    return _return_full_user_or_raise(user_id, user)



# update a users contact details, by specifying the user id
@router.put("/users/{user_id}/contact_details", response_model=UserInfoFull)
async def update_user_contact_details(user_id: int, contact_data: ContactDetailsData, db: Prisma = Depends(get_db)) -> UserInfoFull:
    # create or update the contact details for the user

    await db.contactdetails.upsert(
        where={"userId": user_id},
        data = {
            "create": {
                "user": {"connect": {"id": user_id}},
                "address": contact_data.address,
                "phoneNumber": contact_data.phoneNumber,
            },
            "update": {
                "address": contact_data.address,
                "phoneNumber": contact_data.phoneNumber,
            }, 
        },
    )

    # get the updated user
    user = await db.user.find_unique(
        where={"id": user_id}, 
        include={"contactDetails": True}) # type: ignore[prisma-parsing]

    return _return_full_user_or_raise(user_id, user)



# ---------- DELETE METHODS ----------

# delete a user, by specifying the user id
@router.delete("/users/{user_id}", response_model=UserInfoFull)
async def delete_user(user_id: int, db: Prisma = Depends(get_db)):
    # contact details are deleted automatically they are set to cascade delete in the schema
    user = await db.user.delete(where={"id": user_id})
    return _return_full_user_or_raise(user_id, user)


# delete a users contact details, by specifying the user id
@router.delete("/users/{user_id}/contact_details", response_model=ContactDetailsData)
async def delete_user_contact_details(user_id: int, db: Prisma = Depends(get_db)):
    contact_details = await db.contactdetails.delete(where={"userId": user_id})
    if contact_details is not None:
        return ContactDetailsData(**contact_details.model_dump())
    else:
        raise HTTPException(status_code=404, detail=f"Contact details for user with id '{user_id}' not found")

