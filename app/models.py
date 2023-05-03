from .database import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import TIMESTAMP

# Create ORM model (SQL table) to hold user posts
class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True, nullable=False)
    title=Column(String,nullable=False)
    content=Column(String,nullable=False)
    published=Column(Boolean,server_default='TRUE',nullable=False)
    created_at=Column(TIMESTAMP(timezone=True),nullable=False,
                      server_default=text('now()'))
    user_id = Column(Integer,ForeignKey("users.id",ondelete="CASCADE"),nullable=False)
    owner = relationship("User")
    
# Create ORM Model (SQL table) to hold user account info
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String,nullable=False,unique=True)
    password = Column(String,nullable=False)
    created_at=Column(TIMESTAMP(timezone=True),nullable=False,
                      server_default=text('now()'))
    phone_number = Column(String)
    user_employment_status = Column(String,nullable=True)
    


class Vote(Base):
    __tablename__ = 'votes'
    user_id = Column(Integer,ForeignKey(
        "users.id",ondelete="CASCADE"),primary_key=True)
    post_id = Column(Integer,ForeignKey(
        "posts.id",ondelete="CASCADE"),primary_key=True)