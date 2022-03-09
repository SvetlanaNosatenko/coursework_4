FROM python:3.9-slim-bullseye
ENV FLASK_APP sky_wars.app:app
WORKDIR /opt
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY sky_wars sky_wars


