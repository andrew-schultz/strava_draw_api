To generate a new venv - `python3 -m venv .venv`
To start venv - `source .venv/bin/activate`
To install requirements - `pip3 install -r requirements.txt`
To start server - `python3 src/manage.py runserver`
Access site at - `http://127.0.0.1:8000/` (probably localhost too)

To build images - `docker-compose -f docker-compose.dev.yml build`
To start up - `docker-compose -f docker-compose.dev.yml up`
To bring down - `docker-compose -f docker-compose.dev.yml down`

To start up for a specific dockerfile - `docker-compose up -d --build`
To bring down and remove volumes - `docker-compose down -v`
To bring down for a specific dockerfile - `docker-compose down -v`
To run manage commands - `docker-compose exec web python manage.py migrate --noinput`

To run commands (simple) - `docker-compose exec web python manage.py shell`