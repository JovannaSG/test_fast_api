from pydantic import BaseModel, ConfigDict
from typing import Optional


class TaskBase(BaseModel):
    """Базовая схема для задач"""
    title: str
    description: Optional[str] = None
    completed: bool = False


class TaskCreate(TaskBase):
    """Схема для создания задачи"""
    pass


class TaskUpdate(BaseModel):
    """Схема для обновления задачи"""
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None


class TaskResponse(TaskBase):
    """Схема для ответа с задачей"""
    model_config = ConfigDict(from_attributes=True)

    task_id: int
    title: str
    description: Optional[str]
    completed: Optional[bool]


class TaskList(BaseModel):
    """Схема для списка задач"""
    tasks: list[TaskResponse]
    total: int
