
FROM python:3.10.10-alpine3.17

WORKDIR /usr/app

COPY Pipfile Pipfile.lock ./

RUN pip install pipenv && pipenv install --system --deploy

COPY . .
RUN chmod +x run.sh

ENTRYPOINT ["./run.sh"]
