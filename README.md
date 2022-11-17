## Финальный проект спринта: Проект «api_yamdb».

### Описание.
Проект YaMDb собирает отзывы пользователей на различные произведения. 

Возможности:
 - добавления новых произведений, отзывов
 - ранее добавленным, система оценки произведений 

Произведения делятся на категории:
 - Книги
 - Фильмы
 - Музыка

Произведению может быть присвоен жанр из списка предустановленных.
Новые жанры может создавать только администратор.

Зарегистрированные пользователи оставляют к произведениям  отзывы
и ставят оценку (от 1 до 10). 
По оценкам автоматически высчитывается средняя оценка произведения.

[Документация для API Yamdb в формате Redoc](http://127.0.0.1:8000/redoc/)

### Технологии
[![Python](https://img.shields.io/badge/-Python-464646?style=flat-square&logo=Python)](https://www.python.org/)
[![Django](https://img.shields.io/badge/-Django-464646?style=flat-square&logo=Django)](https://www.djangoproject.com/)
[![Django REST Framework](https://img.shields.io/badge/-Django%20REST%20Framework-464646?style=flat-square&logo=Django%20REST%20Framework)](https://www.django-rest-framework.org/)
### Установка.
### Клонировать репозиторий и перейти в него в командной строке:
```
git clone https://github.com/VadimTT-byte/api_yamdb.git
```
```
cd api_yamdb
```
### Cоздать виртуальное окружение:
```
python -m venv venv
```
### Активировать виртуальное окружение:
```
source venv/scripts/activate
```
### Установить зависимости из файла requirements.txt:
```
pip install -r requirements.txt
```
### Выполнить миграции:
```
python manage.py makemigrations
```
```
python manage.py migrate
```
### Запустить проект:
```
python manage.py runserver
```
## Примеры.
#### Алгоритм регистрации пользователей
- Пользователь отправляет POST-запрос на добавление нового пользователя с параметрами `email` и `username` на эндпоинт ```/api/v1/auth/signup/```.
- **YaMDB** отправляет письмо с кодом подтверждения (`confirmation_code`) на адрес `email`.
 - Пользователь отправляет POST-запрос с параметрами `username` и `confirmation_code` на эндпоинт `/api/v1/auth/token/`, в ответе на запрос ему приходит `token` (JWT-токен).
 - При желании пользователь отправляет PATCH-запрос на эндпоинт `/api/v1/users/me/` и заполняет поля в своём профайле (описание полей — в документации).
#### Пользовательские роли
- Аноним — может просматривать описания произведений, читать отзывы и комментарии.
- Аутентифицированный пользователь (user) — может, как и Аноним, читать всё, дополнительно он может публиковать отзывы и ставить оценку произведениям (фильмам/книгам/песенкам), может комментировать чужие отзывы; может редактировать и удалять свои отзывы и комментарии. Эта роль присваивается по умолчанию каждому новому пользователю.
- Модератор (moderator) — те же права, что и у Аутентифицированного пользователя плюс право удалять любые отзывы и комментарии.
- Администратор (admin) — полные права на управление всем контентом проекта. Может создавать и удалять произведения, категории и жанры. Может назначать роли пользователям.
- Суперюзер Django — обладет правами администратора (admin)
### JWT+djoser sample requests
| Method| Endpoint| Description|
|-----| ------ | ------ |
|POST| /auth/users/| Базовый: зарегистрировать нового пользователя |
|POST| /auth/users/me| Базовый: получить/обновить зарег. пользователя |
|POST| /auth/jwt/create | Создать JWT-токен |
|POST| /auth/jwt/refresh| Получить новый JWT по истечении времени жизни токена |

Documentation [JWT+djoser](https://djoser.readthedocs.io/en/latest/index.html)

  |Method| Endpoint| Description| 
| ------ | ------ | ------ |
| GET| /api/v1/categories/ | Получить список категорий
|	GET |	 /api/v1/genres | Получить список жанров
| GET| api/v1/titles/ | Получить список произведений
| GET | api/v1/titles/{id}/ | Получение информации о произведении по id
| GET | api/v1/titles/{title_id}/reviews/ | Получение всех отзывов к произведению
| GET | api/v1/titles/{title_id}/reviews/{review_id}/comments/ | Получение комментария к отзыву
| GET | api/v1/titles/{title_id}/reviews/{review_id}/comments/{comment_id}/|Получить комментарий для отзыва по id.

### Авторы
[Вадим](https://github.com/VadimTT-byte)
[Кирилл](https://github.com/Kirsumkin)