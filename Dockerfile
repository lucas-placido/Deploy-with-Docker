FROM python:3.8-alpine

WORKDIR /app

COPY . /app 
RUN pip install --no-cache-dir -r ./requirements.txt

ENV FLASK_APP=app.py

EXPOSE 3000

CMD ["flask" "run" "app.py"]

