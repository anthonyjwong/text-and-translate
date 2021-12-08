from datetime import datetime
from os import getenv

from flask import Flask, request

import db.handlers.message_handler as message_handler
import db.handlers.user_handler as user_handler
from db.models import instantiate_tables
from db.sqlalchemy_db import init_db_connection
from nlp.model import init_model
from nlp.translate import translate_conversation

port = getenv("PORT") or 3000

app = Flask(__name__)


@app.route("/conversation/<user_1>/<user_2>", methods=["GET"])
def get_conversation(user_1, user_2):
    if user_1 is None or user_2 is None:
        return {"error": "must provide user_1 and user_2 in request body"}, 400

    conversation = message_handler.get_conversation(user_1, user_2)
    conversation = sorted(conversation, key=lambda x: x["sent_at"])

    tgt_lang = user_handler.get_user_by_id(user_1)["lang"]
    src_lang = user_handler.get_user_by_id(user_2)["lang"]

    print(tgt_lang)
    conversation = translate_conversation(conversation, src_lang, tgt_lang)

    return {"messages": conversation}, 200


@app.route("/last/<user_1>/<user_2>", methods=["GET"])
def get_last_message(user1_id, user2_id):
    if user1_id is None or user2_id is None:
        return {"error": "must provide user_1 and user_2 in request body"}, 400

    conversation = message_handler.get_conversation(user1_id, user2_id)
    conversation = sorted(conversation, key=lambda x: x["sent_at"])

    lang_pref = user_handler.get_user_by_id(user1_id)["lang"]
    conversation = translate_conversation(conversation, lang_pref)

    return {"message": conversation[-2:-1]}, 200


@app.route("/create/<name>", methods=["POST"])
def create_user(name):
    try:
        user = user_handler.create_user(name)
    except Exception:
        return None, 500
    return user, 200


@app.route("/message/send", methods=["POST"])
def send_message():
    try:
        message = message_handler.create_message(
            request.json["sender"],
            request.json["receiver"],
            datetime.now(),
            request.json["content"],
            request.json["lang"]
        )
    except Exception:
        return {"error": "couldn't send message"}, 500
    return {"message_id": message["id"]}, 200


def init_app():
    print("initializing app...")
    init_model()
    init_db_connection()
    instantiate_tables()


def main():
    init_app()
    app.run(host="0.0.0.0", port=port)


if __name__ == "__main__":
    main()
