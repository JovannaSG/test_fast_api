from contextlib import asynccontextmanager
from fastapi import FastAPI

from database import create_tables
from Routers.users_router import router as users_router, roles_router
from Routers.oauth_google_router import router as oauth_google_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan event handler для управления подключением к БД"""
    # Startup
    await create_tables()
    print("TABLES CREATED")
    
    yield
    
    # Shutdown
    print("APP STOPPED")


# Создаем экземпляр FastAPI
app = FastAPI(
    title="FastAPI app",
    version="1.0.0",
    lifespan=lifespan
)
app.include_router(users_router)
app.include_router(roles_router)
app.include_router(oauth_google_router)


@app.get("/")
async def root():
    """Корневой эндпоинт"""
    return {"message": "app started"}
