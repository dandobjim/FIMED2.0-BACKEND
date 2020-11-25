import uuid

from passlib.context import CryptContext
from pydantic import BaseModel, validator
from cryptography.fernet import Fernet
from fimed.database import get_connection


class Token(BaseModel):
    access_token: str
    token_type: str


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# users

class UserBase(BaseModel):
    username: str
    name: str = None
    surname: str = None
    email: str



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
        user_dict["general_form"] = []
        user_dict["patients"] = []
        user_dict["analysis_form"] = []
        user_dict["encryption_key"] = Fernet.generate_key()
        database = get_connection()
        database.users.insert_one(user_dict)

        return UserInDB(**user_dict)


class UserInDB(User):
    password: str

    def verify_password(self, plain_password) -> bool:
        return pwd_context.verify(plain_password, self.password)
