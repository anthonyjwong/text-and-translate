from flask import Flask
from flask import request

app = Flask(__name__)


@app.route('/hello', methods=['GET'])
def hello():
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


@app.route('/hello/<name>', methods=['POST'])
def hello_name(name):
    return {'message': f'Hi, {name}.'}, 200


@app.route('/test', methods=['GET', 'POST'])
def test():
    if request.method == 'GET':
        return {'message': 'test is successful'}, 200
    elif request.method == 'POST':
        msg = request.args.get('msg')
        if msg == None:
            return 'Bad Request', 400
        return {'message': f'{msg}'}, 200
