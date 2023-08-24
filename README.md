# api_yamdb
api_yamdb

### Описание:
Проект YaMDb собирает отзывы пользователей на различные произведения.


### Установка:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone git@github.com:Nastasiya2317/api_yamdb.git
```

```
cd yatube_api/
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv env
```

```
source env/bin/activate
```

Установить зависимости из файла requirements.txt:

```
python3 -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

Выполнить миграции:

```
python3 manage.py migrate
```

Запустить проект:

```
python3 manage.py runserver
```


### Примеры запросов:


Получение списка всех категорий:

```
GET http://127.0.0.1:8000/api/v1/categories/
```

Получение списка всех жанров:

```
GET http://127.0.0.1:8000/api/v1/genres/
```

Список всех произведений:

```
GET http://127.0.0.1:8000/api/v1/titles/
```

Получение списка всех отзывов:

```
GET http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/
```

Получение списка всех комментариев к отзыву:

```
GET http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/{review_id}/comments/
```
