from fastapi import FastAPI, HTTPException, status
from app.schemas import userCreate

app = FastAPI(title="Lab1 - FastAPI User Api")

users: list[userCreate] = []

@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/hello")
def hello():
    return {"message": "Hello World"}


@app.post("/api/users", status_code=status.HTTP_201_CREATED)
def add_user(new_user: userCreate):
    for existing_user in users:
        if existing_user.userid == new_user.userid:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail="A user with this id already exists")
    users.append(new_user)
    return new_user


@app.get("/api/users")
def get_users():
    return users 

@app.get("/api/users/{user_id}")
def get_user(user_id: int):
    for existing_user in users:
        if existing_user.userid == user_id:
            return existing_user 
        
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, 
        detail="User not found",
    )


