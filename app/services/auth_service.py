from app.core.security import hash_password, verify_password, create_access_token
from app.repositories.user_repo import get_user_by_email, create_user
from app.models import User

# checking fuction for user registered or not
def register_user(db, data):
    if get_user_by_email(db, data.user_email):
        return None
    
    # if condition false register the user
    user = User(
        user_name=data.user_name,
        user_email=data.user_email,
        user_password=hash_password(data.user_password),
    )
    return create_user(db, user)

# login function
def login_user(db, data):
    user = get_user_by_email(db, data.user_email)
    if not user:
       return None
    

    if not verify_password(data.user_password, user.user_password):
        return None
    
    token = create_access_token({"sub": str(user.user_id)})
    return token
