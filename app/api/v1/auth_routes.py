from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.services.auth_service import register_user, login_user
from app.schemas.user_schema import UserCreate, UserLogin

router = APIRouter(prefix="/auth", tags=["auth"])


# UserRegister Endpoint
@router.post("/register")
def register(data: UserCreate, db: Session = Depends(get_db)):
    # check user is already registered or not
    user = register_user(db, data)
    if not user:
        raise HTTPException(status_code=400, detail="Email already exists")
    return {"message": "User created"}


# userlogin endpoint
@router.post("/login")
def login(data: UserLogin, db: Session = Depends(get_db)):
    token = login_user(db, data)
    if not token:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    return {"access_token": token}
