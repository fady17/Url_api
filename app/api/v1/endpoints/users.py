from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.db.mongodb import get_mongo_client

router = APIRouter()


class UserModel(BaseModel):
    username: str
    email: str


@router.post("/users")
async def create_user(user: UserModel):
    client = get_mongo_client()
    user_collection = client["url_integrity_checker"]["users"]

    # Insert the new user into the collection
    user_exists = user_collection.find_one({"email": user.email})
    if user_exists:
        raise HTTPException(status_code=400, detail="User already exists.")

    user_collection.insert_one(user.dict())
    return {"message": "User created successfully"}
