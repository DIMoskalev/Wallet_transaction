import re
from typing import Optional

from pydantic import BaseModel, Field, field_validator, ConfigDict


class UserCreate(BaseModel):
    full_name: str
    email: str = Field(...,
                       description="Адрес электронной почты")  # Регулярное выражение для проверки формата электронной почты
    phone: str = Field(...,
                       description="Номер телефона в международном формате, начинающийся с +7 и состоящий из 11 цифр")
    hashed_password: str = Field(..., min_length=8,
                                 description="Пароль должен содержать хотя бы одну заглавную букву и один специальный символ.")

    @field_validator("email")
    @classmethod
    def validate_email(cls, values: str) -> str:
        if not re.match(r'^[\w\.-]+@[\w\.-]+$', values):
            raise ValueError('Неправильный формат электронной почты.')
        return values

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, values: str) -> str:
        if not re.match(r'^\+7\d{10}$', values):
            raise ValueError('Неправильный формат телефона. Пример: +71234567890')
        return values

    @field_validator("hashed_password")
    @classmethod
    def validate_password(cls, values: str) -> str:
        if not any(char.isupper() for char in values):
            raise ValueError('Пароль должен содержать хотя бы одну заглавную букву.')
        if not any(char in "$%&!:" for char in values):
            raise ValueError('Пароль должен содержать хотя бы один специальный символ: $ % & ! :')
        return values


class UserGet(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    full_name: str
    email: str
    phone: str
    is_admin: bool  # Поле для указания, является ли пользователь администратором


class UserLogin(BaseModel):
    email: None | str = Field(Optional[str], description="Электронная почта")
    phone: None | str = Field(Optional[str], description="Номер телефона")
    hashed_password: str = Field(..., min_length=8, max_length=30, description="Пароль, от 5 до 30 символов")
