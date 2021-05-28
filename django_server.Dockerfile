FROM python:3.9.5 AS base
WORKDIR /code
COPY Pipfile* ./
RUN pip install pipenv
RUN pipenv install --system --deploy
COPY . ./
RUN chmod +x entrypoint.sh
ENTRYPOINT ["./entrypoint.sh"]

FROM base AS development
RUN pipenv install --system --deploy --dev

FROM base AS production
RUN apt-get update \
    && apt-get install -y nginx \
    && apt-get install -y ufw \
    && mkdir -p /run/uwsgi \
    && ln -s $(pwd)/conf/nginx_shop_bot.conf /etc/nginx/sites-enabled
