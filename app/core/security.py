from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta, timezone

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = "Mein Nhi Bataunga"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


# Function to convert plain password to hash password
def hash_password(password: str):
    # 🔒 bcrypt supports max 72 bytes
    password_bytes = password.encode("utf-8")[:72]
    return pwd_context.hash(password_bytes)


# Function to verify password
def verify_password(plain: str, hashed: str):
    plain_bytes = plain.encode("utf-8")[:72]
    return pwd_context.verify(plain_bytes, hashed)


# Access token
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
