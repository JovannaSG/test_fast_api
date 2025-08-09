# FastAPI приложение

FastAPI приложение с SQLAlchemy ORM, асинхронной работой с базой

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
│   ├── users_router.py           # Роуты для управления задачами
│   └── oauth_google_router.py    # Роут для получения Google OAuth2 URL
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
   - Создайте базу данных: `your_db_name`
   - Создайте пользователя или используйте существующего

3. **Настройте переменные окружения:**
   Создайте файл `.env` в корне проекта:
   ```
   DB_HOST=localhost
   DB_PORT=5432
   DB_NAME=your_db_name
   DB_USER=your_username
   DB_PASSWORD=your_password
   ```

## Запуск приложения

```bash
python run.py
```

Или через uvicorn:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

# API Examples

## API для ролей

### Создать роль
```bash
curl -X POST "http://localhost:8000/roles/" \
-H "Content-Type: application/json" \
-d '{
  "name": "admin"
}'
```

### Получить все роли
```bash
curl -X GET "http://localhost:8000/roles/"
```

### Получить роль по ID
```bash
curl -X GET "http://localhost:8000/roles/1"
```

---

## API для пользователей

### Создать пользователя
```bash
curl -X POST "http://localhost:8000/users/" \
-H "Content-Type: application/json" \
-d '{
  "full_name": "Иван Петров",
  "phone_number": "+7 (999) 123-45-67",
  "email": "ivan.petrov@example.com",
  "description": "Главный администратор системы",
  "role_id": 1
}'
```

### Получить всех пользователей
```bash
curl -X GET "http://localhost:8000/users/?skip=0&limit=10"
```

### Получить пользователя по ID
```bash
curl -X GET "http://localhost:8000/users/1"
```

### Получить пользователя по email
```bash
curl -X GET "http://localhost:8000/users/email/ivan.petrov@example.com"
```

### Получить пользователя по телефону
```bash
curl -X GET "http://localhost:8000/users/phone/+7%20(999)%20123-45-67"
```

### Получить пользователей по роли
```bash
curl -X GET "http://localhost:8000/users/by-role/1"
```

### Получить пользователей по названию роли
```bash
curl -X GET "http://localhost:8000/users/by-role-name/admin"
```

### Обновить пользователя
```bash
curl -X PUT "http://localhost:8000/users/1" \
-H "Content-Type: application/json" \
-d '{
  "full_name": "Иван Петрович Иванов",
  "description": "Обновленное описание"
}'
```

### Изменить роль пользователя
```bash
curl -X PATCH "http://localhost:8000/users/1/role?new_role_id=2"
```

### Удалить пользователя
```bash
curl -X DELETE "http://localhost:8000/users/1"
```

---

## Валидация данных

### Правила валидации для пользователей:

- **ФИО**: минимум 2 слова, максимум 150 символов
- **Телефон**: 7-20 символов, может содержать цифры, пробелы, скобки, дефисы, плюс
- **Email**: стандартная валидация email
- **Роль**: должна существовать в базе данных

### Примеры корректных данных:

```json
{
  "full_name": "Анна Сергеевна Смирнова",
  "phone_number": "+7 (912) 345-67-89",
  "email": "anna.smirnova@company.ru",
  "description": "Менеджер по продажам",
  "role_id": 2
}
```

### Примеры некорректных данных:

```json
{
  "full_name": "Анна",  // Ошибка: должно быть минимум 2 слова
  "phone_number": "123",  // Ошибка: неверный формат
  "email": "invalid-email",  // Ошибка: неверный формат email
  "role_id": 999  // Ошибка: роль не существует
}
```

---

## Структура ответов

### Пользователь с ролью:
```json
{
  "id": 1,
  "full_name": "Иван Петров",
  "phone_number": "+7 (999) 123-45-67",
  "email": "ivan.petrov@example.com",
  "description": "Главный администратор системы",
  "role_id": 1,
  "created_at": "2024-01-01T12:00:00Z",
  "updated_at": "2024-01-01T12:00:00Z",
  "role": {
    "id": 1,
    "name": "admin"
  }
}
```

### Список пользователей:
```json
{
  "users": [...],
  "total": 25
}
```