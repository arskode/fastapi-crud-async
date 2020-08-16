FROM python:3.8.3-buster

ENV PYTHONUNBUFFERED 1

WORKDIR /usr/src/app

COPY ./requirements.txt /usr/src/app/requirements.txt

RUN pip install --upgrade pip setuptools wheel \
    && pip install -r requirements.txt

COPY . /usr/src/app/

CMD uvicorn src.main:app --reload --reload-dir src --workers 1 --host 0.0.0.0 --port 5000
