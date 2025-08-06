from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from repository import TaskRepository
from schemas import TaskCreate, TaskUpdate, TaskResponse, TaskList

router = APIRouter(
    prefix="/tasks",
    tags=["tasks"]
)


@router.get("/", response_model=TaskList)
async def get_tasks(
    skip: int = Query(0, ge=0, description="Количество записей для пропуска"),
    limit: int = Query(
        100, ge=1, le=1000,
        description="Максимальное количество записей"
    ),
    db: AsyncSession = Depends(get_db)
) -> None:
    """Получить все задачи с пагинацией"""
    repo = TaskRepository(db)
    tasks = await repo.get_all(skip=skip, limit=limit)
    total = await repo.count()
    return TaskList(
        tasks=[
            TaskResponse.model_validate(
                task,
                from_attributes=True
            ) for task in tasks
        ],
        total=total
    )


@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(
    task_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Получить задачу по ID"""
    repo = TaskRepository(db)
    task = await repo.get_by_id(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Задача не найдена")
    return TaskResponse.model_validate(task, from_attributes=True)


@router.post("/", response_model=TaskResponse, status_code=201)
async def create_task(
    task: TaskCreate,
    db: AsyncSession = Depends(get_db)
):
    """Создать новую задачу"""
    repo = TaskRepository(db)
    new_task = await repo.create(task)
    return TaskResponse.model_validate(new_task, from_attributes=True)


@router.put("/{task_id}", response_model=TaskResponse)
async def update_task(
    task_id: int,
    task_update: TaskUpdate,
    db: AsyncSession = Depends(get_db)
):
    """Обновить задачу"""
    repo = TaskRepository(db)
    updated_task = await repo.update(task_id, task_update)
    if not updated_task:
        raise HTTPException(status_code=404, detail="Задача не найдена")
    return TaskResponse.model_validate(updated_task, from_attributes=True)


@router.delete("/{task_id}")
async def delete_task(
    task_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Удалить задачу"""
    repo = TaskRepository(db)
    task = await repo.get_by_id(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Задача не найдена")
    success = await repo.delete(task_id)
    if success:
        return {"message": f"Задача '{task.title}' удалена"}
    else:
        raise HTTPException(status_code=404, detail="Задача не найдена")


@router.patch("/{task_id}/complete", response_model=TaskResponse)
async def complete_task(
    task_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Отметить задачу как выполненную"""
    repo = TaskRepository(db)
    result = await repo.complete(task_id)
    if not result:
        raise HTTPException(status_code=404, detail="Задача не найдена")
    return TaskResponse.model_validate(result, from_attributes=True)
