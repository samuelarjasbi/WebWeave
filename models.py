# models.py
from sqlalchemy import Column, Integer, ForeignKey, UniqueConstraint,String
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, unique=True, nullable=False)
    full_name = Column(String, nullable=False)
    
    # Relationships (simplified)
    following = relationship(
        "User",
        secondary="relationships",
        primaryjoin="User.user_id == Relationship.follower_id",
        secondaryjoin="User.user_id == Relationship.followed_id",
        back_populates="followers"
    )
    followers = relationship(
        "User",
        secondary="relationships",
        primaryjoin="User.user_id == Relationship.followed_id",
        secondaryjoin="User.user_id == Relationship.follower_id",
        back_populates="following"
    )

class Relationship(Base):
    __tablename__ = "relationships"
    id = Column(Integer, primary_key=True, autoincrement=True)
    follower_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    followed_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    
    __table_args__ = (
        UniqueConstraint("follower_id", "followed_id", name="_follower_followed_uc"),
    )