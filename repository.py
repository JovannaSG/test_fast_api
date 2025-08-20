from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from sqlalchemy.orm import selectinload
from typing import List, Optional

from models import UserModel, RoleModel
from schemas import UserCreate, UserUpdate, RoleCreate, RoleUpdate


class RoleRepository:
    """Репозиторий для работы с ролями"""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all(self) -> List[RoleModel]:
        """Получить все роли"""
        query = select(RoleModel).order_by(RoleModel.role_id)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_by_id(self, role_id: int) -> Optional[RoleModel]:
        """Получить роль по ID"""
        query = select(RoleModel).where(RoleModel.role_id == role_id)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def get_by_name(self, name: str) -> Optional[RoleModel]:
        """Получить роль по названию"""
        query = select(RoleModel).where(RoleModel.role_name == name)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def create(self, role_data: RoleCreate) -> RoleModel:
        """Создать новую роль"""
        role = RoleModel(role_name=role_data.role_name)
        self.session.add(role)
        await self.session.commit()
        await self.session.refresh(role)
        return role

    async def update(
        self,
        role_id: int,
        role_data: RoleUpdate
    ) -> Optional[RoleModel]:
        """Обновить роль"""
        role = await self.get_by_id(role_id)
        if not role:
            return None

        update_data = role_data.model_dump(exclude_unset=True)
        if update_data:
            query = (
                update(RoleModel)
                .where(RoleModel.role_id == role_id)
                .values(**update_data)
            )
            await self.session.execute(query)
            await self.session.commit()
            return await self.get_by_id(role_id)
        
        return role

    async def delete(self, role_id: int) -> bool:
        """Удалить роль"""
        query = delete(RoleModel).where(RoleModel.role_id == role_id)
        result = await self.session.execute(query)
        await self.session.commit()
        return result.rowcount > 0

    async def count(self) -> int:
        """Получить общее количество ролей"""
        query = select(RoleModel.role_id)
        result = await self.session.execute(query)
        return len(result.scalars().all())


class UserRepository:
    """Репозиторий для работы с пользователями"""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all(
        self,
        skip: int = 0,
        limit: int = 100,
        include_role: bool = False
    ) -> List[UserModel]:
        """Получить всех пользователей с пагинацией"""
        query = select(UserModel).offset(skip).limit(limit).order_by(UserModel.user_id)
        
        if include_role:
            query = query.options(selectinload(UserModel.role))
        
        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_by_id(self, user_id: int, include_role: bool = False) -> Optional[UserModel]:
        """Получить пользователя по ID"""
        query = select(UserModel).where(UserModel.user_id == user_id)
        
        if include_role:
            query = query.options(selectinload(UserModel.role))
            
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def get_by_email(self, email: str, include_role: bool = False) -> Optional[UserModel]:
        """Получить пользователя по email"""
        query = select(UserModel).where(UserModel.email == email)
        
        if include_role:
            query = query.options(selectinload(UserModel.role))
            
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def get_by_phone(self, phone_number: str, include_role: bool = False) -> Optional[UserModel]:
        """Получить пользователя по номеру телефона"""
        query = select(UserModel).where(UserModel.phone_number == phone_number)
        
        if include_role:
            query = query.options(selectinload(UserModel.role))
            
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def create(self, user_data: UserCreate) -> UserModel:
        """Создать нового пользователя"""
        user = UserModel(
            full_name=user_data.full_name,
            phone_number=user_data.phone_number,
            email=user_data.email,
            description=user_data.description,
            role_id=user_data.role_id
        )
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user
    
    async def update(
        self,
        user_id: int,
        user_data: UserUpdate
    ) -> Optional[UserModel]:
        """Обновить пользователя"""
        # Получаем текущего пользователя
        user = await self.get_by_id(user_id)
        if not user:
            return None

        # Обновляем только переданные поля
        update_data = user_data.model_dump(exclude_unset=True)
        if update_data:
            query = (
                update(UserModel)
                .where(UserModel.user_id == user_id)
                .values(**update_data)
            )
            await self.session.execute(query)
            await self.session.commit()
            
            # Возвращаем обновленного пользователя
            return await self.get_by_id(user_id)
        
        return user

    async def delete(self, user_id: int) -> bool:
        """Удалить пользователя"""
        query = delete(UserModel).where(UserModel.user_id == user_id)
        result = await self.session.execute(query)
        await self.session.commit()
        return result.rowcount > 0
    
    async def change_role(
        self,
        user_id: int,
        new_role_id: int
    ) -> Optional[UserModel]:
        """Изменить роль пользователя"""
        query = (
            update(UserModel)
            .where(UserModel.user_id == user_id)
            .values(role_id=new_role_id)
        )
        result = await self.session.execute(query)
        await self.session.commit()
        
        if result.rowcount > 0:
            return await self.get_by_id(user_id, include_role=True)
        return None
    
    async def count(self) -> int:
        """Получить общее количество пользователей"""
        query = select(UserModel.user_id)
        result = await self.session.execute(query)
        return len(result.scalars().all())

    async def get_by_role_id(self, role_id: int, include_role: bool = False) -> List[UserModel]:
        """Получить пользователей по ID роли"""
        query = select(UserModel).where(UserModel.role_id == role_id)
        
        if include_role:
            query = query.options(selectinload(UserModel.role))
            
        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_by_role_name(self, role_name: str, include_role: bool = False) -> List[UserModel]:
        """Получить пользователей по названию роли"""
        query = (
            select(UserModel)
            .join(RoleModel)
            .where(RoleModel.role_name == role_name.lower())
        )
        
        if include_role:
            query = query.options(selectinload(UserModel.role))
            
        result = await self.session.execute(query)
        return result.scalars().all()

    async def verify_role_exists(self, role_id: int) -> bool:
        """Проверить существование роли"""
        query = select(RoleModel.role_id).where(RoleModel.role_id == role_id)
        result = await self.session.execute(query)
        return result.scalar_one_or_none() is not None
