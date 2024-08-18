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


app.conf.beat_schedule = {
    'run-my-task-every-30-seconds': {
        'task': 'orders.tasks.initiate_auto_payments',
        'schedule': 30.0,  # Запуск задачи каждые 30 секунд
    },
}

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
