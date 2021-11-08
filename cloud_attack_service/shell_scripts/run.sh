#!/bin/bash

/opt/wait_for_db.sh

echo "#############################################################"
echo "# Running migrations"
echo "#############################################################"
python manage.py migrate

echo "#############################################################"
echo "# Web-server started"
echo "#############################################################"

gunicorn -c /opt/django/gunicorn.conf.py cloud_attack_service.wsgi:application

