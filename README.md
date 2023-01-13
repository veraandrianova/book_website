# Вебсайт о книгах

## Backend:
Python 3.10, Django 4.0.6, SQLite

Подробный перечень используемых библиотек находятся в файле requirements.txt

## Функционал
   - возможность авторизации
   - возможность просматривать информацию о книгах, авторах, издательствах
   - возможность добавлять книги
   - возможность оставлять комментарии

## Инструкция по развертыванию

##### Клонируйте проект из репозитория.

##### Установите необходимые зависимости.
    pip install -r requirements.txt

##### Создать миграции
    python manage.py makemigration
    python manage.py migrate

#### Создать суперпользователя
    python manage.py createsuperuser

#### Создать миграции
    python manage.py migrate

#### Запустить приложение 
    python manage.py runserver
    
#### Запустить тесты 
    python manage.py test    

##### Стили https://proproprogs.ru/
