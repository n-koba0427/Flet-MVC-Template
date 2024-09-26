"""
Authentication Module

This module provides authentication functionality for the application.
It includes two main classes:

1. Auth: A base class for authentication that defines the basic structure
   and common methods for user authentication.

2. SaltedHashAuth: A subclass of Auth that implements salted hash authentication.

The module uses the User model and utility functions from app.utils.
"""

import hashlib
import os
from app.utils import *


# Base Authentication
class Auth:
    """
    Base Authentication class.
    
    This class provides a foundation for authentication methods.
    It includes methods for user retrieval, user addition, and password verification.
    Some methods are left to be implemented by subclasses.
    """
    
    def get_user(self, username: str):
        return search_data("user", "username", username).get()
    
    def add_user(self, data_dict: dict):
        data_dict = self._get_data_dict(data_dict)
        add_data("user", data_dict)

    def _get_data_dict(self, data_dict: dict):
        raise NotImplementedError("This method must be implemented in the subclass")

    def verify_password(self, username_attempt: str, password_attempt: str):
        user = self.get_user(username_attempt)
        if exists(user):
            status = self._check_password(user, password_attempt)
            return self.get_result(user, status)
        return {"user": None, "msg": "User not found"}
    
    def _check_password(self, user: User, password_attempt: str) -> bool:
        raise NotImplementedError("This method must be implemented in the subclass")
    
    def get_result(self, user: User, status: bool):
        user = user if status else None
        msg = "Password is correct" if status else "Password is incorrect"
        return {"user": user, "msg": msg}


# Salted Hash Authentication
class SaltedHashAuth(Auth):
    """
    Salted Hash Authentication class.
    
    This class implements salted hash authentication.
    It extends the base Auth class and provides concrete implementations
    for password hashing, checking, and data preparation.
    """
    
    def hash_password(self, password: str):
        salt = os.urandom(16)
        hashed_password = hashlib.sha256(salt + password.encode()).hexdigest()
        return salt.hex(), hashed_password

    def _check_password(self, user: User, password_attempt: str):
        stored_salt = bytes.fromhex(user.salt)
        password_attempt = hashlib.sha256(stored_salt + password_attempt.encode()).hexdigest()
        return password_attempt == user.password
    
    def _get_data_dict(self, data_dict: dict):
        salt, hashed_password = self.hash_password(data_dict["password"])
        data_dict["salt"] = salt
        data_dict["password"] = hashed_password
        return data_dict