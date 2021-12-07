from nlp.model import normalize


def translate_conversation(convo: "list[str]", lang: str):
    translated = []
    for msg in convo:
        if msg["lang"] == lang:  # no need to translate
            translated.append(msg)
            continue

        norm_msg = normalize(msg["message_content"])

    return translated
