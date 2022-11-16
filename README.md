## Финальный проект спринта: Проект «API для Yatube».

### Описание.

Этот проект позволяет пользоваться приложением Yatube:
* получение списка публикаций или отдельной публикации по id;
* добавление, обновление и удаление публикаций;
* получение списка доступных сообществ и получение информации о сообществе по id;
* получение всех комментариев к публикации или комментария к публикации по id;
* добавление, обновление и удаление комментариев;
* подписка на пользователей

### Установка.

### Клонировать репозиторий и перейти в него в командной строке:

git clone https://github.com/VadimTT-byte/api_yamdb.git

cd api_final_yatube

### Cоздать виртуальное окружение:

python -m venv venv

### Активировать виртуальное окружение:

source venv/scripts/activate

### Установить зависимости из файла requirements.txt:

pip install -r requirements.txt

### Выполнить миграции:

python manage.py makemigrations

python manage.py migrate

### Запустить проект:

python manage.py runserver

### Примеры.

Документация размещена по адресу:
http://127.0.0.1:8000/redoc/
