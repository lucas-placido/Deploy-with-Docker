FROM python:3.10-slim-buster

WORKDIR /app

COPY . /app 
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*
RUN /usr/local/bin/python -m pip install --upgrade pip
RUN pip install -r requirements.txt


ENV FLASK_APP=app.py

EXPOSE 5000


CMD ["python", "./flask/app.py"]

