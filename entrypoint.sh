#!/usr/bin/env bash
python manage.py migrate
python manage.py initdb ./shop_data/fixtures/items.yaml
python manage.py createsuperuserifnone

if [[ "${STAGE}" == "development" ]]; then
  python manage.py runserver 0.0.0.0:8000 --noreload
elif [[ "${STAGE}" == "production" ]]; then
  echo yes | python manage.py collectstatic
  /etc/init.d/nginx start
  uwsgi --ini ./conf/uwsgi_shop_bot.ini
else
  echo "Incorrect environment variable STAGE value"
fi
