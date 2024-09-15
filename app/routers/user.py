from fastapi import APIRouter, HTTPException
from app.schemas import CreateUser, UpdateUser

router = APIRouter(prefix="/user", tags=["user"])

users = []

@router.get("/")
async def all_users():
    return users

@router.get("/{user_id}")
async def user_by_id(user_id: int):
    user = next((user for user in users if user.id == user_id), None)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.post("/create", response_model=dict)
async def create_user(user: CreateUser):
    user_id = len(users) + 1
    new_user = user.dict()
    new_user["id"] = user_id
    users.append(new_user)
    return new_user

@router.put("/update/{user_id}", response_model=dict)
async def update_user(user_id: int, user: UpdateUser):
    for u in users:
        if u["id"] == user_id:
            u.update(user.dict())
            return u
    raise HTTPException(status_code=404, detail="User not found")

@router.delete("/delete/{user_id}", response_model=dict)
async def delete_user(user_id: int):
    for u in users:
        if u["id"] == user_id:
            users.remove(u)
            return u
    raise HTTPException(status_code=404, detail="User not found")