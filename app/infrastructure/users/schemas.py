from pydantic import BaseModel, EmailStr, field_validator

from app.common.enums.user_enums import UserStatusesEnum
from app.core.exceptions import PasswordFormatError, NameFormatError


def validate_password(password: str) -> str:
    if len(password) < 8:
        raise PasswordFormatError("Password too short")

    if not any(ch.isdigit() for ch in password):
        raise PasswordFormatError("Password must contain digits")

    if not any(ch in "!@#$%^&*()?" for ch in password):
        raise PasswordFormatError("Password must contain special symbols")

    return password


def validate_name(name: str) -> str:
    if any(letter.isdigit() or letter.isspace() for letter in name):
        raise NameFormatError('Name has digits or spaces')

    return name


class CreateUserSchema(BaseModel):
    """Класс схема для проверки полей при создании пользователя"""

    key: UserStatusesEnum
    name: str
    email: EmailStr
    password: str

    @field_validator('name')
    @classmethod
    def validate_name(cls, name: str) -> str:
        return validate_name(name)

    @field_validator('password')
    @classmethod
    def validate_password(cls, password: str) -> str:
        return validate_password(password)


class LoginUserSchema(BaseModel):
    """Класс схема для проверки полей при входе в аккаунт пользователя"""

    email: EmailStr
    password: str

    @field_validator('password')
    @classmethod
    def validate_password(cls, password: str) -> str:
        return validate_password(password)


class CloseUserSchema(BaseModel):
    """Класс схема для проверки полей при закрытии аккаунта пользователя"""

    name: str
    email: EmailStr
    password: str

    @field_validator('name')
    @classmethod
    def validate_name(cls, name: str) -> str:
        return validate_name(name)