Помимо пакетов из requirements.txt для запуска также потребуется докер-контейнер redis. Для его установки нужны команды:
sudo apt install docker.io
docker run -p 6379:6379 -d redis:2.8

Ссылка на документацию к API:
https://documenter.getpostman.com/view/4241636/RWgtTx3g