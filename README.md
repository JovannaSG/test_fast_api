# FastAPI с SQLAlchemy и PostgreSQL

Современное FastAPI приложение с SQLAlchemy ORM, асинхронной работой с базой данных и миграциями Alembic.

## Структура проекта

```
.
├── main.py                        # Основной файл приложения
├── models.py                      # SQLAlchemy ORM модели
├── schemas.py                     # Pydantic схемы для API
├── database.py                    # Конфигурация SQLAlchemy
├── repository.py                  # CRUD операции
├── config.py                      # Конфигурация подключения к БД
├── oauth_google.py                # Генерация OAuth2 URL для Google
├── run.py                         # Скрипт запуска приложения
├── Routers/                       # Папка с роутерами FastAPI
│   ├── tasks_router.py           # Роуты для управления задачами
│   └── oauth_google_router.py    # Роут для получения Google OAuth2 URL
├── alembic.ini                    # Конфигурация миграций
├── alembic/                       # Папка с миграциями
├── requirements.txt               # Зависимости проекта
└── README.md                      # Документация
```

## Установка и настройка

1. **Установите зависимости:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Настройте PostgreSQL:**
   - Установите PostgreSQL
   - Создайте базу данных: `taskdb`
   - Создайте пользователя или используйте существующего

3. **Настройте переменные окружения:**
   Создайте файл `.env` в корне проекта:
   ```
   DB_HOST=localhost
   DB_PORT=5432
   DB_NAME=taskdb
   DB_USER=your_username
   DB_PASSWORD=your_password
   ```

4. **Инициализируйте миграции:**
   ```bash
   alembic init alembic
   alembic revision --autogenerate -m "Initial migration"
   alembic upgrade head
   ```

## Запуск приложения

```bash
python run.py
```

Или через uvicorn:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## API Endpoints

### Основные
- `GET /` - Корневой эндпоинт
- `GET /health` - Проверка состояния

### Аутентификация через Google
- `GET /auth/google/url` - Получить ссылку для авторизации через Google

### Управление задачами
- `GET /tasks` - Получить все задачи (с пагинацией)
- `GET /tasks/{task_id}` - Получить задачу по ID
- `POST /tasks` - Создать новую задачу
- `PUT /tasks/{task_id}` - Обновить задачу
- `DELETE /tasks/{task_id}` - Удалить задачу
- `PATCH /tasks/{task_id}/complete` - Отметить задачу как выполненную

### Параметры пагинации
- `skip` - количество записей для пропуска (по умолчанию: 0)
- `limit` - максимальное количество записей (по умолчанию: 100, максимум: 1000)

## Миграции

### Создание новой миграции
```bash
alembic revision --autogenerate -m "Описание изменений"
```

### Применение миграций
```bash
alembic upgrade head
```

### Откат миграции
```bash
alembic downgrade -1
```

### Просмотр истории миграций
```bash
alembic history
```

## Особенности проекта

### SQLAlchemy ORM
- Асинхронная работа с базой данных
- Автоматическое создание таблиц
- Типизированные модели
- Поддержка миграций

### Pydantic схемы
- Валидация данных на уровне API
- Автоматическая документация
- Разделение входных и выходных данных

### Repository Pattern
- Инкапсуляция логики работы с БД
- Легкое тестирование
- Переиспользование кода

### Роутеры FastAPI
- Модульная структура API
- Разделение логики по функциональности
- Легкое масштабирование

### OAuth2 интеграция
- Поддержка Google OAuth2
- Генерация авторизационных ссылок
- Расширяемая архитектура для других провайдеров

### Современные практики
- Dependency Injection
- Lifespan event handlers
- Асинхронная архитектура
- Типизация

## Документация API

После запуска приложения документация доступна по адресу:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Примеры использования

### Получение OAuth2 ссылки Google
```bash
curl "http://localhost:8000/auth/google/url"
```

### Создание задачи
```bash
curl -X POST "http://localhost:8000/tasks" \
     -H "Content-Type: application/json" \
     -d '{"title": "Изучить SQLAlchemy", "description": "Изучить основы SQLAlchemy ORM"}'
```

### Получение задач с пагинацией
```bash
curl "http://localhost:8000/tasks?skip=0&limit=10"
```

### Обновление задачи
```bash
curl -X PUT "http://localhost:8000/tasks/1" \
     -H "Content-Type: application/json" \
     -d '{"title": "Обновленное название", "completed": true}'
``` 