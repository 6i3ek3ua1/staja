from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# устанавливаем модуль настроек Django для celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'staja.settings')

app = Celery('staja')

# Загружаем настройки из settings.py
app.config_from_object('django.conf:settings', namespace='CELERY')

# Автоматически обнаруживаем и загружаем задачи из всех приложений Django
app.autodiscover_tasks()
