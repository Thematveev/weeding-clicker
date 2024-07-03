from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
# from sqlalchemy.orm import relationship

from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String, index=True)
    score = Column(Integer, nullable=False)
    userId = Column(String, nullable=False, unique=True, index=True)