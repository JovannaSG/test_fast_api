from pydantic import BaseModel, ConfigDict, EmailStr, Field, validator
from typing import Optional
from datetime import datetime
import re


# Схемы для ролей
class RoleBase(BaseModel):
    """Базовая схема для ролей"""
    role_name: str = Field(
        min_length=1,
        max_length=50,
        description="Название роли"
    )


class RoleCreate(RoleBase):
    """Схема для создания роли"""
    role_name: str


class RoleUpdate(BaseModel):
    """Схема для обновления роли"""
    role_name: Optional[str] = Field(None, min_length=1, max_length=50)


class RoleResponse(RoleBase):
    """Схема для ответа с ролью"""
    model_config = ConfigDict(from_attributes=True)

    role_id: int
    role_name: str


class RoleList(BaseModel):
    """Схема для списка ролей"""
    roles: list[RoleResponse]
    total: int


# Схемы для пользователей
class UserBase(BaseModel):
    """Базовая схема для пользователей"""
    full_name: str = Field(
        min_length=2,
        max_length=150,
        description="ФИО (минимум 2 слова)"
    )
    phone_number: str = Field(
        min_length=7,
        max_length=20,
        description="Номер телефона"
    )
    email: EmailStr = Field(description="Электронная почта")
    description: Optional[str] = Field(None, description="Описание")
    role_id: int = Field(gt=0, description="ID роли")

    @validator('full_name')
    def validate_full_name(cls, v):
        """Проверка что ФИО содержит минимум 2 слова"""
        if not re.match(r'^\S+(?:\s+\S+){1,}$', v):
            raise ValueError('ФИО должно содержать минимум 2 слова')
        return v

    @validator('phone_number')
    def validate_phone_number(cls, v):
        """Проверка формата номера телефона"""
        if not re.match(r'^\+?[0-9\s\-\(\)]{7,20}$', v):
            raise ValueError('Неверный формат номера телефона')
        return v


class UserCreate(UserBase):
    """Схема для создания пользователя"""
    pass


class UserUpdate(BaseModel):
    """Схема для обновления пользователя"""
    full_name: Optional[str] = Field(None, min_length=2, max_length=150)
    phone_number: Optional[str] = Field(None, min_length=7, max_length=20)
    email: Optional[EmailStr] = None
    description: Optional[str] = None
    role_id: Optional[int] = Field(None, gt=0)

    @validator('full_name')
    def validate_full_name(cls, v):
        """Проверка что ФИО содержит минимум 2 слова"""
        if v is not None and not re.match(r'^\S+(?:\s+\S+){1,}$', v):
            raise ValueError('ФИО должно содержать минимум 2 слова')
        return v

    @validator('phone_number')
    def validate_phone_number(cls, v):
        """Проверка формата номера телефона"""
        if v is not None and not re.match(r'^\+?[0-9\s\-\(\)]{7,20}$', v):
            raise ValueError('Неверный формат номера телефона')
        return v


class UserResponse(BaseModel):
    """Схема для ответа с пользователем"""
    model_config = ConfigDict(from_attributes=True)

    user_id: int
    full_name: str
    phone_number: str
    email: str
    description: Optional[str]
    role_id: int
    created_at: datetime
    updated_at: datetime
    
    # Информация о роли (если загружена)
    role: Optional[RoleResponse] = None


class UserWithRoleResponse(UserResponse):
    """Схема для ответа с пользователем, обязательно включающая роль"""
    role: RoleResponse


class UserList(BaseModel):
    """Схема для списка пользователей"""
    users: list[UserResponse]
    total: int


class UserListWithRoles(BaseModel):
    """Схема для списка пользователей с ролями"""
    users: list[UserWithRoleResponse]
    total: int


# ======= LOGIN SCHEMAS =======

class UserLoginSchema(BaseModel):
    username: str
    password: str
