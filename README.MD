# need to create postgres database first

sudo -u postgres -i

psql

CREATE DATABASE etc.

then 

python manage.py makemigrations
python manage.py migrate
python manage.py runserver

(would probably work with gunicorn also)


