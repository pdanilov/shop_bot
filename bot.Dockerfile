FROM python:3.9.5 AS base
WORKDIR /code
COPY Pipfile* ./
RUN pip install pipenv
RUN pipenv install --system --deploy
COPY . ./
RUN chmod +x manage.py
ENTRYPOINT ["./manage.py"]
CMD ["runbot"]

FROM base AS development
RUN pipenv install --system --deploy --dev

FROM base AS production
