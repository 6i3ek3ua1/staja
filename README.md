# task-3


# Команды ngrok:

Ngrok включение:
```
ngrok http http://localhost:8000 
```
Ngrok выключение:
```
taskkill /f /im ngrok.exe 
```

# Docker:
Старт:
```
 docker-compose up --build 
```
Выключение:
```
docker-compose down
```
Миграции:
```
docker exec -it staja-web-1 python manage.py makemigrations
docker exec -it staja-web-1 python manage.py migrate
```
Суперпользователь:
```
docker exec -it staja-web-1 python manage.py createsuperuser
```
Чистка бд:
```
docker-compose exec web python manage.py flush --no-input
```
# Celery (на всякий пожарный)

Включение worker и beat (необходим работающий сервер redis)
```
celery -A <project_name> worker --loglevel=info 
celery -A <project_name> beat --loglevel=info
```
Выключение:
```
tasklist | findstr celery
taskkill /PID <PID> /F
```
