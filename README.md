# DRF LMS

Учебный проект: API для управления курсами и уроками на Django REST Framework.

## Технологии

- Python 3.10+
- Django
- Django REST Framework
- SQLite
- Pillow

## Установка и запуск

### 1. Клонирование
```bash
git clone https://github.com/DenWhite77/drf-lms.git
cd drf-lms
```

### 2. Виртуальное окружение
```bash
python -m venv .venv
.venv\Scripts\activate      # Windows
source .venv/bin/activate   # Linux / macOS
```

### 3. Зависимости
```bash
pip install -r requirements.txt
```

### 3. Миграции и запуск
```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## API Эндпоинты

### Курсы
- `GET /api/courses/` — список курсов
- `POST /api/courses/` — создание курса
- `GET /api/courses/{id}/` — получение курса
- `PUT /api/courses/{id}/` — обновление курса
- `DELETE /api/courses/{id}/` — удаление курса

### Уроки
- `GET /api/lessons/` — список уроков
- `POST /api/lessons/` — создание урока
- `GET /api/lessons/{id}/` — получение урока
- `PATCH /api/lessons/{id}/` — обновление урока
- `DELETE /api/lessons/{id}/` — удаление урока

### Пользователи (доп. задание)
- `GET /api/users/{id}/` — профиль пользователя
- `PATCH /api/users/{id}/` — обновление профиля пользователя

## API Эндпоинты

### Курсы
- `GET /api/courses/` — список курсов (с полями `lessons_count` и вложенными `lessons`)
- `POST /api/courses/` — создание курса
- `GET /api/courses/{id}/` — получение курса
- `PUT /api/courses/{id}/` — обновление курса
- `DELETE /api/courses/{id}/` — удаление курса

### Уроки
- `GET /api/lessons/` — список уроков
- `POST /api/lessons/` — создание урока
- `GET /api/lessons/{id}/` — получение урока
- `PATCH /api/lessons/{id}/` — обновление урока
- `DELETE /api/lessons/{id}/` — удаление урока

### Пользователи
- `GET /api/users/{id}/` — профиль пользователя (с историей платежей)
- `PATCH /api/users/{id}/` — обновление профиля пользователя

### Платежи
- `GET /api/payments/` — список платежей
  - `?ordering=payment_date` — сортировка по дате (возрастание)
  - `?ordering=-payment_date` — сортировка по дате (убывание)
  - `?course={id}` — фильтр по ID курса
  - `?lesson={id}` — фильтр по ID урока
  - `?payment_method=cash|transfer` — фильтр по способу оплаты

## Наполнение базы тестовыми данными

Для создания тестовых пользователей, курсов, уроков и платежей используйте кастомную команду:
```bash
python manage.py create_test_data
```

## Аутентификация и права доступа

В проекте используется **JWT-аутентификация** (`djangorestframework-simplejwt`).

### Получение токена
- `POST /api/token/` — принимает `{"email": "...", "password": "..."}` и выдает пару `access/refresh`.
- `POST /api/token/refresh/` — обновляет `access` токен по `refresh`.

### Роли
- **Аноним** — может только зарегистрироваться (`POST /api/register/`) или получить токен.
- **Пользователь** — видит, редактирует и удаляет **только свои** курсы и уроки.
- **Модератор** (группа `Модераторы`) — видит все курсы и уроки, может их **редактировать**, но **не может создавать и удалять**.

### Права на эндпоинты
- Все эндпоинты, кроме `/api/token/` и `/api/register/`, требуют заголовок `Authorization: Bearer <access_token>`.
- Для `CourseViewSet` права настраиваются по `action` (`create`, `update`, `destroy`, `list`/`retrieve`).
- Для `Lesson` права настраиваются по HTTP-методу (`GET`, `POST`, `PUT/PATCH`, `DELETE`).
- Проверка прав реализована в `lms/permissions.py` (классы `IsModerator` и `IsOwner`).

### Заполнение группы «Модераторы»
- Фикстура: `users/fixtures/groups.json`.
- Загрузить: `python manage.py loaddata users/fixtures/groups.json`.
- Назначить пользователя в группу через админку (`/admin/`).

## Дополнительные возможности (ДЗ 4)

- **Валидация ссылок**: В уроках можно указывать только видео с YouTube (`youtube.com`, `youtu.be`). Валидатор в `lms/validators.py`.
- **Подписки**: Пользователи могут подписываться на обновления курсов. Эндпоинт `POST /api/subscriptions/` (принимает `course_id`). Подписка автоматически создается или удаляется, если она уже существует.
- **Признак подписки**: В API курса (`GET /api/courses/`) добавлено поле `is_subscribed` (True/False).
- **Пагинация**: Настроена для списка курсов и уроков (по 3 элемента на страницу).
- **Тестирование**: Покрытие тестами (CRUD уроков, валидация, подписки, права доступа). Отчет в `coverage.txt`.

## Интеграция со Stripe и Документация

### Новые эндпоинты:
- `POST /api/payments/create/` — создание платежа. Принимает `course_id` или `lesson_id`. Возвращает ссылку на оплату (`payment_link`).
- `GET /api/payments/status/{session_id}/` — получение статуса сессии оплаты.

### Документация API (Swagger):
Доступна по адресам:
- Swagger UI: `http://127.0.0.1:8000/api/docs/`
- ReDoc: `http://127.0.0.1:8000/api/redoc/`
- Схема (YAML): `http://127.0.0.1:8000/api/schema/`

### Переменные окружения:
Для работы Stripe в файле `.env` должны быть указаны:
- `STRIPE_SECRET_KEY`
- `STRIPE_PUBLISHABLE_KEY`
- 
## Автор
DenWhite77