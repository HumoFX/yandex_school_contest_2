# Yandex School Contest - 2 API
Restful API for yandex school contest 2

## Getting started
After activating venv install modules
```
pip install -r requierements.txt
```

Fill in `.env` file. For reference take a look at `.env`
```
DEBUG=False
DB_LOCAL=True
...
```

Run migrations
```
python manage.py migrate
```

Run the server
```
python manage.py runserver
```
##Alternative run server with gunicorn
```
sh run.sh
```

## Run in docker

```
export TAG=local
docker-compose build && docker-compose up
```
