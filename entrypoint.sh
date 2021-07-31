#!/bin/sh

#if [ "$DATABASE" = "postgres" ]
#then
    echo "Waiting for postgres..."

    while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
#fi

#python manage.py flush --no-input
python manage.py makemigrations 
python manage.py migrate
#crear un superusuario aqui 
python manage.py g_superuser
#creando los datos random
#python manage.py g_random1

#python manage.py collectstatic --noinput

exec "$@"
