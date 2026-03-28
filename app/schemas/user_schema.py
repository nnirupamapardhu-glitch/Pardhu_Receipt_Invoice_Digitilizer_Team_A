from pydantic import BaseModel, EmailStr, Field

# Registration
class UserCreate(BaseModel):
    user_name: str
    user_email: EmailStr
    user_password: str = Field(..., min_length=6, max_length=72)
# Login
class UserLogin(BaseModel):
    user_email: EmailStr
    user_password: str
