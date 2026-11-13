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

## Автор
DenWhite77