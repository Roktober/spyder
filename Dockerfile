FROM python:3.8.1-alpine

RUN apk add --update --no-cache linux-headers
RUN apk add --update --no-cache g++ gcc libxslt-dev
RUN apk add --update --no-cache postgresql-dev python3-dev musl-dev


RUN mkdir /app

COPY ./requirements.txt ./requirements-dev.txt /app/

WORKDIR /app

RUN pip install --upgrade pip
RUN pip install -r requirements.txt -r requirements-dev.txt

COPY . /app/

CMD ["python", "/app/src/main.py", "--help"]
