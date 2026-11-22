import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('config')

app.config_from_object('django.conf:settings', namespace='CELERY')

# ВОТ ЭТА СТРОКА ЗАСТАВИТ REDIS 6.x ИСПОЛЬЗОВАТЬ СТАРЫЙ ПРОТОКОЛ:
app.conf.broker_transport_options = {'protocol': 2}
app.conf.result_backend_transport_options = {'protocol': 2}

app.autodiscover_tasks()
