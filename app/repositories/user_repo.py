from app.models import User

# function to search user based on email and fetch from db 
def get_user_by_email(db, email):
    return db.query(User).filter(User.user_email == email).first()


def create_user(db, user):
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
