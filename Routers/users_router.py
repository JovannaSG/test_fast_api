from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from pydantic import ValidationError

from database import get_db
from repository import UserRepository, RoleRepository
from schemas import (
    UserCreate, UserUpdate, UserResponse, UserList, 
    UserWithRoleResponse, UserListWithRoles,
    RoleCreate, RoleUpdate, RoleResponse, RoleList
)

router = APIRouter(
    prefix="/users",
    tags=["users"]
)

roles_router = APIRouter(
    prefix="/roles",
    tags=["roles"]
)


# === ROLES ENDPOINTS ===

@roles_router.get("/", response_model=RoleList)
async def get_roles(db: AsyncSession = Depends(get_db)):
    """Получить все роли"""
    repo = RoleRepository(db)
    roles = await repo.get_all()
    total = await repo.count()
    return RoleList(
        roles=[
            RoleResponse.model_validate(role, from_attributes=True) 
            for role in roles
        ],
        total=total
    )


@roles_router.get("/{role_id}", response_model=RoleResponse)
async def get_role(role_id: int, db: AsyncSession = Depends(get_db)):
    """Получить роль по ID"""
    repo = RoleRepository(db)
    role = await repo.get_by_id(role_id)
    if not role:
        raise HTTPException(status_code=404, detail="Роль не найдена")
    return RoleResponse.model_validate(role, from_attributes=True)


@roles_router.post("/", response_model=RoleResponse, status_code=201)
async def create_role(role: RoleCreate, db: AsyncSession = Depends(get_db)):
    """Создать новую роль"""
    repo = RoleRepository(db)
    
    # Проверяем уникальность названия роли
    existing_role = await repo.get_by_name(role.role_name)
    if existing_role:
        raise HTTPException(
            status_code=400, 
            detail="Роль с таким названием уже существует"
        )
    
    try:
        new_role = await repo.create(role)
        return RoleResponse.model_validate(new_role, from_attributes=True)
    except IntegrityError:
        raise HTTPException(
            status_code=400,
            detail="Ошибка создания роли. Проверьте уникальность названия."
        )


@roles_router.put("/{role_id}", response_model=RoleResponse)
async def update_role(
    role_id: int, 
    role_update: RoleUpdate, 
    db: AsyncSession = Depends(get_db)
):
    """Обновить роль"""
    repo = RoleRepository(db)
    
    # Проверяем существование роли
    existing_role = await repo.get_by_id(role_id)
    if not existing_role:
        raise HTTPException(status_code=404, detail="Роль не найдена")
    
    # Проверяем уникальность названия, если оно обновляется
    if role_update.role_name:
        name_role = await repo.get_by_name(role_update.role_name)
        if name_role and name_role.role_id != role_id:
            raise HTTPException(
                status_code=400,
                detail="Роль с таким названием уже существует"
            )
    
    try:
        updated_role = await repo.update(role_id, role_update)
        if not updated_role:
            raise HTTPException(status_code=404, detail="Роль не найдена")
        return RoleResponse.model_validate(updated_role, from_attributes=True)
    except IntegrityError:
        raise HTTPException(
            status_code=400,
            detail="Ошибка обновления роли. Проверьте уникальность названия."
        )


@roles_router.delete("/{role_id}")
async def delete_role(role_id: int, db: AsyncSession = Depends(get_db)):
    """Удалить роль"""
    repo = RoleRepository(db)
    role = await repo.get_by_id(role_id)
    if not role:
        raise HTTPException(status_code=404, detail="Роль не найдена")
    
    try:
        success = await repo.delete(role_id)
        if success:
            return {"message": f"Роль '{role.role_name}' удалена"}
        else:
            raise HTTPException(status_code=404, detail="Роль не найдена")
    except IntegrityError:
        raise HTTPException(
            status_code=400,
            detail="Невозможно удалить роль. К ней привязаны пользователи."
        )


# === ЭНДПОИНТЫ ДЛЯ ПОЛЬЗОВАТЕЛЕЙ ===

@router.get("/", response_model=UserListWithRoles)
async def get_users(
    skip: int = Query(0, ge=0, description="Количество записей для пропуска"),
    limit: int = Query(
        100, ge=1, le=1000,
        description="Максимальное количество записей"
    ),
    db: AsyncSession = Depends(get_db)
):
    """Получить всех пользователей с пагинацией"""
    repo = UserRepository(db)
    users = await repo.get_all(skip=skip, limit=limit, include_role=True)
    total = await repo.count()
    return UserListWithRoles(
        users=[
            UserWithRoleResponse.model_validate(
                user,
                from_attributes=True
            ) for user in users
        ],
        total=total
    )


@router.get("/{user_id}", response_model=UserWithRoleResponse)
async def get_user(
    user_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Получить пользователя по ID"""
    repo = UserRepository(db)
    user = await repo.get_by_id(user_id, include_role=True)
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    return UserWithRoleResponse.model_validate(user, from_attributes=True)


@router.get("/email/{email}", response_model=UserWithRoleResponse)
async def get_user_by_email(
    email: str,
    db: AsyncSession = Depends(get_db)
):
    """Получить пользователя по email"""
    repo = UserRepository(db)
    user = await repo.get_by_email(email, include_role=True)
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь с таким email не найден")
    return UserWithRoleResponse.model_validate(user, from_attributes=True)


@router.get("/phone/{phone_number}", response_model=UserWithRoleResponse)
async def get_user_by_phone(
    phone_number: str,
    db: AsyncSession = Depends(get_db)
):
    """Получить пользователя по номеру телефона"""
    repo = UserRepository(db)
    user = await repo.get_by_phone(phone_number, include_role=True)
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь с таким номером телефона не найден")
    return UserWithRoleResponse.model_validate(user, from_attributes=True)


@router.get("/by-role/{role_id}", response_model=list[UserWithRoleResponse])
async def get_users_by_role_id(
    role_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Получить пользователей по ID роли"""
    repo = UserRepository(db)
    role_repo = RoleRepository(db)
    
    # Проверяем существование роли
    role = await role_repo.get_by_id(role_id)
    if not role:
        raise HTTPException(status_code=404, detail="Роль не найдена")
    
    users = await repo.get_by_role_id(role_id, include_role=True)
    return [
        UserWithRoleResponse.model_validate(user, from_attributes=True) 
        for user in users
    ]


@router.get("/by-role-name/{role_name}", response_model=list[UserWithRoleResponse])
async def get_users_by_role_name(
    role_name: str,
    db: AsyncSession = Depends(get_db)
):
    """Получить пользователей по названию роли"""
    repo = UserRepository(db)
    users = await repo.get_by_role_name(role_name, include_role=True)
    return [
        UserWithRoleResponse.model_validate(user, from_attributes=True) 
        for user in users
    ]


@router.post("/", response_model=UserWithRoleResponse, status_code=201)
async def create_user(
    user: UserCreate,
    db: AsyncSession = Depends(get_db)
):
    """Создать нового пользователя"""
    repo = UserRepository(db)
    role_repo = RoleRepository(db)
    
    # Проверяем существование роли
    role_exists = await repo.verify_role_exists(user.role_id)
    if not role_exists:
        raise HTTPException(
            status_code=400,
            detail="Указанная роль не существует"
        )
    
    # Проверяем уникальность email и телефона
    existing_email = await repo.get_by_email(user.email)
    if existing_email:
        raise HTTPException(
            status_code=400, 
            detail="Пользователь с таким email уже существует"
        )
    
    existing_phone = await repo.get_by_phone(user.phone_number)
    if existing_phone:
        raise HTTPException(
            status_code=400, 
            detail="Пользователь с таким номером телефона уже существует"
        )
    
    try:
        new_user = await repo.create(user)
        # Получаем пользователя с ролью для ответа
        user_with_role = await repo.get_by_id(new_user.id, include_role=True)
        return UserWithRoleResponse.model_validate(user_with_role, from_attributes=True)
    except IntegrityError:
        raise HTTPException(
            status_code=400,
            detail="Ошибка создания пользователя. Проверьте уникальность данных."
        )
    except ValidationError as e:
        raise HTTPException(
            status_code=422,
            detail=f"Ошибка валидации данных: {str(e)}"
        )


@router.put("/{user_id}", response_model=UserWithRoleResponse)
async def update_user(
    user_id: int,
    user_update: UserUpdate,
    db: AsyncSession = Depends(get_db)
):
    """Обновить пользователя"""
    repo = UserRepository(db)
    
    # Проверяем существование пользователя
    existing_user = await repo.get_by_id(user_id)
    if not existing_user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    
    # Проверяем существование роли, если она обновляется
    if user_update.role_id:
        role_exists = await repo.verify_role_exists(user_update.role_id)
        if not role_exists:
            raise HTTPException(
                status_code=400,
                detail="Указанная роль не существует"
            )
    
    # Проверяем уникальность email, если он обновляется
    if user_update.email:
        email_user = await repo.get_by_email(user_update.email)
        if email_user and email_user.user_id != user_id:
            raise HTTPException(
                status_code=400,
                detail="Пользователь с таким email уже существует"
            )
    
    # Проверяем уникальность телефона, если он обновляется
    if user_update.phone_number:
        phone_user = await repo.get_by_phone(user_update.phone_number)
        if phone_user and phone_user.user_id != user_id:
            raise HTTPException(
                status_code=400,
                detail="Пользователь с таким номером телефона уже существует"
            )
    
    try:
        updated_user = await repo.update(user_id, user_update)
        if not updated_user:
            raise HTTPException(status_code=404, detail="Пользователь не найден")

        # Получаем пользователя с ролью для ответа
        user_with_role = await repo.get_by_id(user_id, include_role=True)
        return UserWithRoleResponse.model_validate(user_with_role, from_attributes=True)
    except IntegrityError:
        raise HTTPException(
            status_code=400,
            detail="Ошибка обновления пользователя. Проверьте уникальность данных."
        )
    except ValidationError as e:
        raise HTTPException(
            status_code=422,
            detail=f"Ошибка валидации данных: {str(e)}"
        )


@router.delete("/{user_id}")
async def delete_user(
    user_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Удалить пользователя"""
    repo = UserRepository(db)
    user = await repo.get_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    
    success = await repo.delete(user_id)
    if success:
        return {"message": f"Пользователь '{user.full_name}' удален"}
    else:
        raise HTTPException(status_code=404, detail="Пользователь не найден")


@router.patch("/{user_id}/role", response_model=UserWithRoleResponse)
async def change_user_role(
    user_id: int,
    new_role_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Изменить роль пользователя"""
    repo = UserRepository(db)
    
    # Проверяем существование роли
    role_exists = await repo.verify_role_exists(new_role_id)
    if not role_exists:
        raise HTTPException(
            status_code=400,
            detail="Указанная роль не существует"
        )
    
    result = await repo.change_role(user_id, new_role_id)
    if not result:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    return UserWithRoleResponse.model_validate(result, from_attributes=True)
