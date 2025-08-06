from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from typing import List, Optional

from models import TaskModel
from schemas import TaskCreate, TaskUpdate


class TaskRepository:
    """Репозиторий для работы с задачами"""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all(
        self,
        skip: int = 0,
        limit: int = 100
    ) -> List[TaskModel]:
        """Получить все задачи с пагинацией"""
        query = (
            select(TaskModel).offset(skip)
            .limit(limit)
            .order_by(TaskModel.task_id)
        )
        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_by_id(self, task_id: int) -> Optional[TaskModel]:
        """Получить задачу по ID"""
        query = select(TaskModel).where(TaskModel.task_id == task_id)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def create(self, task_data: TaskCreate) -> TaskModel:
        """Создать новую задачу"""
        task = TaskModel(
            title=task_data.title,
            description=task_data.description,
            completed=task_data.completed
        )
        self.session.add(task)
        await self.session.commit()
        await self.session.refresh(task)
        return task
    
    async def update(
        self,
        task_id: int,
        task_data: TaskUpdate
    ) -> Optional[TaskModel]:
        """Обновить задачу"""
        # Получаем текущую задачу
        task = await self.get_by_id(task_id)
        if not task:
            return None

        # Обновляем только переданные поля
        update_data = task_data.model_dump(exclude_unset=True)
        if update_data:
            query = (
                update(TaskModel)
                .where(TaskModel.task_id == task_id)
                .values(**update_data)
            )
            await self.session.execute(query)
            await self.session.commit()
            
            # Возвращаем обновленную задачу
            return await self.get_by_id(task_id)
        
        return task

    async def delete(self, task_id: int) -> bool:
        """Удалить задачу"""
        query = delete(TaskModel).where(TaskModel.task_id == task_id)
        result = await self.session.execute(query)
        await self.session.commit()
        return result.rowcount > 0
    
    async def complete(self, task_id: int) -> Optional[TaskModel]:
        """Отметить задачу как выполненную"""
        query = (
            update(TaskModel)
            .where(TaskModel.task_id == task_id)
            .values(completed=True)
        )
        result = await self.session.execute(query)
        await self.session.commit()
        
        if result.rowcount > 0:
            return await self.get_by_id(task_id)
        return None
    
    async def count(self) -> int:
        """Получить общее количество задач"""
        query = select(TaskModel.task_id)
        result = await self.session.execute(query)
        return len(result.scalars().all())
