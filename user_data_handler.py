# user_data_handler.py
from db_manager import DatabaseManager

class UserDataHandler:
    def __init__(self):
        self.db = DatabaseManager()

    def sanitize_string(self, value):
        """Removes null characters from a string."""
        return value.replace("\x00", "") if isinstance(value, str) else value

    def debug_check(self, value, name):
        """Checks for null characters in the string and prints a warning if found."""
        if isinstance(value, str) and "\x00" in value:
            print(f"Warning: Null character found in {name}: {repr(value)}")

    def enter_user_info(self, username, full_name, followers, followings):
        # Sanitize and debug check main user
        username = self.sanitize_string(username)
        full_name = self.sanitize_string(full_name)
        self.debug_check(username, "username")
        self.debug_check(full_name, "full_name")

        # Add the main user
        self.db.add_user(username, full_name)

        # Process followers (users who follow the target)
        for follower in followers:
            follower["username"] = self.sanitize_string(follower["username"])
            follower["full_name"] = self.sanitize_string(follower["full_name"])
            self.debug_check(follower["username"], "follower username")
            self.debug_check(follower["full_name"], "follower full_name")

            self.db.add_user(follower["username"], follower["full_name"])
            self.db.add_relationship(follower["username"], username)  # follower → target

        # Process followings (users the target follows)
        for following in followings:
            following["username"] = self.sanitize_string(following["username"])
            following["full_name"] = self.sanitize_string(following["full_name"])
            self.debug_check(following["username"], "following username")
            self.debug_check(following["full_name"], "following full_name")

            self.db.add_user(following["username"], following["full_name"])
            self.db.add_relationship(username, following["username"])  # target → following

    def close(self):
        """Closes the database connection."""
        self.db.close()
