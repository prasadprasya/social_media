# pull official base image
FROM python:3.8.3-alpine

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev
# RUN pip install psycopg2
RUN apk add gcc musl-dev libffi-dev openssl-dev python3-dev

COPY ./requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# copy project
COPY . .
# run entrypoint.sh
ENTRYPOINT ["/usr/src/app/entrypoint.sh"]