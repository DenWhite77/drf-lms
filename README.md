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

## Автор
DenWhite77