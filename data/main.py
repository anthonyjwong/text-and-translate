from db.sqlalchemy_db import init_db_connection
from db.models import instantiate_tables
from flask import Flask
from flask import request
from os import getenv

port = getenv("PORT") or 3000

app = Flask(__name__)


@app.route('/send/<user>', methods=['POST'])
def send(user):
    return {'message': f'Hi, {user}.'}, 200


@app.route('/receive/<user>', methods=['GET'])
def receive(user):
    return {
        'messages': [
            {
                'messageContent': 'test sent message',
                'messageType': 'sender'
            },
            {
                'messageContent': 'test received message',
                'messageType': 'receiver'
            }
        ]
    }, 200


def init_app():
    init_db_connection()
    instantiate_tables()


def main():
    init_app()
    app.run(host="0.0.0.0", port=port)


if __name__ == "__main__":
    main()
