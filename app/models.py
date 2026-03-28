from sqlalchemy import Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import relationship
from app.db.session import Base

# Base Model for user creation
class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    user_name = Column(String, nullable=False)
    user_email = Column(String, unique=True, index=True)
    user_password = Column(String, nullable=False)
    invoices = relationship("Invoice", back_populates="user")
    role = Column(String, default="user")

# Base model for file upload
class File(Base):
    __tablename__ = "files"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String)
    owner_id = Column(Integer, ForeignKey("users.user_id"))


# Invoice Model
class Invoice(Base):
    __tablename__ = "invoices"

    id = Column(Integer, primary_key=True, index=True)
    invoice_number = Column(String, nullable=True)
    vendor_name = Column(String, nullable=True)
    date = Column(String, nullable=True)
    total_amount = Column(Float, nullable=True)
    file_path = Column(String, nullable=True)

    user_id = Column(Integer, ForeignKey("users.user_id"))

    user = relationship("User", back_populates="invoices")
