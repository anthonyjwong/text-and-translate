# syntax=docker/dockerfile:1
FROM python:3

# Create app directory
WORKDIR /app

# Install app dependencies
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

ENV FLASK_APP=main.py

CMD [ "python", "-m", "flask", "run", "--host=0.0.0.0", "--port=3000"]