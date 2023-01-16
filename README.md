## Backend карточной игры [Twelve](https://card-game.ru)

### Локальный запуск

#### Подготовка
1. Клонировать репозиторий на свой компьютер  
`git clone https://github.com/apodisation13/cardgame/`
2. Перейти в директорию `backend/`  
`cd backend/`
3. Создать файл `.env` с переменными окружения, аналогичный [.env.template](backend/.env.template)
4. Открыть на Google Sheets [файл с данными игры](https://docs.google.com/spreadsheets/d/1gQtc5_fB4OxdnL9KfIaXLPBkXhFJWfKT4cnN1YpA0Iw/edit?usp=share_link) 
и скачать его в формате `OpenDocument (.ods)` в директорию `backend/`
5. Скачать [архив с медиафайлами игры](https://drive.google.com/file/d/1N5iP8KwWCF-emr3xY0kM5r867T4G4oio/view?usp=share_link)
и распаковать его в директорию `backend/`


#### Запуск
1. Перейти в директорию `docker/`  
`cd ../docker/`
2. Выполнить команду  
`docker-compose --env-file ../backend/.env up --build -d`
3. Создать суперпользователя для входа в административную панель  
`docker exec -it cardgame_backend python manage.py createsuperuser`

После успешного запуска сервера доступны следующие адреса:

- [127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/) - административная панель Django, 
- [127.0.0.1:8000/api/schema/swagger-ui/](http://127.0.0.1:8000/api/schema/swagger-ui/) - документация API.
