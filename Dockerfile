FROM python:3.7-slim

COPY . /app

WORKDIR /app

RUN pip install --upgrade pip
RUN pip install -r requirements/requirements.txt
RUN pip install -e .

