# messg-api

Example API with Django and Django Ninja. 

API Docs: https://messg-api.herokuapp.com/api/docs

Available endpoints:
- **/api/messages/** _GET_ - List all added messages
- **/api/messages/{message_id}/** _GET_ - Retrive message, increments counter
- **/api/messages/{message_id}/** _POST_* - Add message
- **/api/messages/{message_id}/** _PUT_* - Update message, restet counter
- **/api/messages/{message_id}/** _DELETE_* - Delete message

\* API key required

---

### Development

SQLite database and Django development server.

Recomended [poetry](https://github.com/python-poetry/poetry) for local development.

You will need to add API key by django shell or manually in database.

#### poetry

1. Go to project root directory
2. Install and set environment:
   ```sh
   $ poetry install
   $ poetry shell
   $ cd messgapi
   ```
3. Run tests:
   ```sh
   $ python manage.py tests
   ```
4. Create a database:
   ```sh
   $ python manage.py migrate
   ```
4. Run development server:
   ```sh
   $ python manage.py runserver
   ```
5. The server should be running on: [localhost:8000](http://localhost:8000/)


#### docker

1. Go to project root directory
2. Build images:
    ```sh
   $ docker-compose build
   ```
3. Run containers:
    ```sh
    $ docker-compose up -d
    ```
4. Create a database:
    ```sh
    $ docker exec messg-api python manage.py migrate
    ```
5. The server should be running on: [localhost:8000](http://localhost:8000/)

---

### Deployment

Heroku, PostgreSQL and gunicorn.

[Build manifest](https://devcenter.heroku.com/articles/build-docker-images-heroku-yml) in heroku.yml.
