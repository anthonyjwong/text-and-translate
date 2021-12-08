from nlp.model import get_translator, translate


def translate_conversation(convo: "list[str]", src_lang: str, tgt_lang: str):
    translated = []
    encoder, decoder = get_translator(src_lang, tgt_lang)
    for i, msg in enumerate(convo):
        if msg["lang"] == tgt_lang:  # no need to translate
            translated.append(msg)
            continue

        translation = translate(
            msg["message_content"], encoder, decoder, src_lang, tgt_lang)

        translated.append(msg)
        translated[i]["message_content"] = " ".join(translation)

    return translated
