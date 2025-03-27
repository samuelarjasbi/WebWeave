# db_manager.py
from database import get_session
from models import User, Relationship  # Import the correct model
from typing import Optional

class DatabaseManager:
    def __init__(self):
        self.session = get_session()

    def add_user(self, username, full_name):
        """Adds a new user if not already in the database."""
        user = self.get_user(username)
        if not user:
            user = User(username=username, full_name=full_name)
            self.session.add(user)
            self.session.commit()
            print(f"New user {username} added.")
        else:
            print(f"User {username} already exists.")
        return user

    def get_user(self, username):
        """Retrieves a user by username."""
        return self.session.query(User).filter_by(username=username).first()

    def add_relationship(self, follower_username, followed_username):
        """Adds a follow relationship (follower -> followed)."""
        follower = self.get_user(follower_username)
        followed = self.get_user(followed_username)
        
        if not follower:
            raise ValueError(f"Follower {follower_username} not found.")
        if not followed:
            raise ValueError(f"Followed user {followed_username} not found.")
        
        # Check if relationship exists
        existing = self.session.query(Relationship).filter_by(
            follower_id=follower.user_id,
            followed_id=followed.user_id
        ).first()
        
        if not existing:
            new_rel = Relationship(
                follower_id=follower.user_id,
                followed_id=followed.user_id
            )
            self.session.add(new_rel)
            self.session.commit()
            print(f"Relationship added: {follower_username} -> {followed_username}")
        else:
            print(f"Relationship exists: {follower_username} -> {followed_username}")
            
    def get_user_by_id(self, user_id: int) -> Optional[User]:
        """Retrieve user by their ID"""
        return self.session.query(User).filter_by(user_id=user_id).first()
    def close(self):
        """Closes the database session."""
        self.session.close()