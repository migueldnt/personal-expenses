# Personal expenses

Django system that allows recording income and expenses.

## Technologies

- Backend: Django, python 
- Frontend: bulma css, vue js

## how to run for developers

* Prerequisites: Postgres database


Create python virtual environment

```bash
#python3.6 should be available
virtualenv virtualenv -p python3.6 env
```
Activate and install

```bash
source env/bin/activate
pip install -r requirements.txt
```

Create environment variables 

```bash
cp .env-example .env
```

Fill the `.env` file with your data and export
```bash
export $(cat .env | xargs)
```

create migrations and superuser

```bash
python manage.py makemigrations 
python manage.py migrate
python manage.py g_superuser
```

Local deploy
```bash
python manage.py runserver
```
