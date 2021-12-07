# syntax=docker/dockerfile:1
FROM python:3.7

# Create app directory
WORKDIR /app

# Install app dependencies
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Download spacy dependencies
RUN python3 -m spacy download en_core_web_sm
RUN python3 -m spacy download es_core_news_sm

COPY . .

ENV FLASK_APP=main.py

CMD [ "stdbuf", "-oL", "python", "-u", "main.py" ]