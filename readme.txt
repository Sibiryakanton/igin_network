Используемые пакеты:
Django
Django-channels
Redis
Django Rest Framework
Celery

Для запуска за боевом сервере также потребуется
sudo apt install docker.io

Запуск redis-контейнера:
docker run -p 6379:6379 -d redis:2.8