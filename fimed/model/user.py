from passlib.context import CryptContext
from pydantic import BaseModel, validator
from typing import List

from fimed.database import get_connection
from fimed.model.patient import PatientModel

# security


class Token(BaseModel):
    access_token: str
    token_type: str


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# users


class UserBase(BaseModel):
    username: str
    fullname: str = None
    email: str
<<<<<<< HEAD
<<<<<<< HEAD
    patients: list
=======
>>>>>>> a0697f63e9cda236fd62dc84adf56a81795ee170
=======
>>>>>>> 94bba846af767aa5e26a1a474e68499bd5d1614d


class UserCreateRequest(UserBase):
    password: str

    @validator("username")
    def username_alphanumeric(cls, v):
        assert v.isalpha(), "must be alphanumeric"
        return v

    @validator("email")
    def email_is_valid(cls, v):
        assert "@" in v, "email is not valid"
        return v

    @property
    def hashed_password(self) -> str:
        return pwd_context.hash(self.password)


class User(UserBase):
    disabled: bool = False

    @staticmethod
    def get(username: str):
        """
        Gets user from database.
        """
        database = get_connection()
        user = database.users.find_one({"username": username})

        if user:
            return UserInDB(**user)

    @staticmethod
    def save(user: UserCreateRequest):
        """
        Saves user to database.
        """
        user_dict = user.dict()
        user_dict["password"] = user.hashed_password

        database = get_connection()
        database.users.insert_one(user_dict)

        return UserInDB(**user_dict)


class UserInDB(User):
    password: str

    def verify_password(self, plain_password) -> bool:
        return pwd_context.verify(plain_password, self.password)
