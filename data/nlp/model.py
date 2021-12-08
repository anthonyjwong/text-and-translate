from json import loads
from random import shuffle

from spacy import load
from torch import device, long, no_grad, tensor, zeros
from torch.cuda import is_available as cuda_is_available
from torch.nn.modules.loss import CrossEntropyLoss
from torch.optim import SGD

from nlp.rnn import Decoder, Encoder
from nlp.vocab import EOS_TOKEN, SOS_TOKEN, Vocab

DEVICE = device("cuda" if cuda_is_available() else "cpu")

DATASET_FILE = "nlp/tatoeba.txt"
LANGS = ["en", "es"]
SRC_LANG = "en"
TGT_LANG = "es"
MAX_DATASET_SIZE = 5000


def load_dataset(filename, src_lang, tgt_lang):
    """
    Loads dataset.
    File must consist of line-separated translations, where each
    sentence is tab-separated.
    Ex:
        Hello!  ¡Hola!
        How are you?    ¿Cómo estás?
        ...

    :param filename: name of dataset file
    :param src_lang: language code for first language appearing in file
    :param tgt_lang: language code for second language appearing in file
    :return: json list
    """
    global max_length
    max_length = 0

    dataset = []
    with open(filename, "r") as file:
        datum = file.readline()
        i = 0
        while i < MAX_DATASET_SIZE and datum:
            datum = datum.split('\t')
            if len(datum[0]) > max_length:
                max_length = len(datum[0])
            if len(datum[1]) > max_length:
                max_length = len(datum[1])

            dataset.append({
                src_lang: normalize(datum[0], src_lang),
                tgt_lang: normalize(datum[1], tgt_lang)
            })

            if i % 10000 == 0:
                print(f"{i} lines processed.")

            datum = file.readline()
            i += 1
    return dataset


def normalize(string, lang):
    """
    Normalizes string. Proper nouns stay capitalized.

    :param string: string to normalize
    :param lang: language of string
    :return: string
    """
    doc = tokenizer[lang](string)

    normalized = []
    for token in doc:
        if token.pos_ == "PROPN":
            normalized.append(token.text)
        elif token.is_punct:
            continue
        else:
            normalized.append(token.text.lower())

    return " ".join(normalized)


def get_lang_data(dataset, lang):
    """
    Yields iterable of specified language data.

    :param dataset: dataset obtained from load_dataset
    :param lang: language code of desired data
    :return: iterable
    """
    for datum in dataset:
        yield datum[lang]


def create_vocabs(dataset):
    """
    Creates vocabulary for each of the langauges in the dataset.

    :param dataset: dataset obtained from load_dataset
    :return: dictionary
    """
    vocabs = {}
    for lang in LANGS:
        data_iter = get_lang_data(dataset, lang)
        vocabs[lang] = Vocab(data_iter, lang)
    return vocabs


def convert_to_tensor(string, lang):
    """
    Converts dataset to tensor for model input.

    :param dataset: dataset to convert
    :param vocab: vocab of each lang
    """
    indices = []
    for word in string.split(" "):
        try:
            indices.append(vocab[lang].word2index[word])
        except Exception:
            continue
    indices.append(EOS_TOKEN)

    return tensor(indices, dtype=long,
                  device=DEVICE).view(-1, 1)


def convert_to_tensors(dataset):
    """
    Converts dataset to tensor for model input in place.

    :param dataset: dataset to convert
    :param vocab: vocab of each lang
    """
    for lang in LANGS:
        for datum in dataset:
            datum[lang] = convert_to_tensor(datum[lang], lang)


def get_train_test(dataset, split=.8):
    """
    Splits dataset into training set and testing set.

    :param dataset: dataset to split
    :split: percent of data to go in training set
    :return: tensor training set, tensor test set
    """
    convert_to_tensors(dataset)

    shuffle(dataset)    # shuffles in place
    train_test_split = int(split * len(dataset))
    train = dataset[:train_test_split]
    test = dataset[train_test_split:]

    return train, test


def train(input_tensor, target_tensor, encoder, decoder,
          encoder_optimizer, decoder_optimizer, loss_fn):
    memory = encoder.init_memory()

    encoder_optimizer.zero_grad()
    decoder_optimizer.zero_grad()

    encoder_outputs = zeros(
        decoder.max_len, encoder.memory_size, device=DEVICE)

    loss = 0
    for i in range(input_tensor.size(0)):
        output, memory = encoder(input_tensor[i], memory)
        encoder_outputs[i] = output[0, 0]

    decoder_input = tensor([[SOS_TOKEN]], device=DEVICE)
    for i in range(target_tensor.size(0)):
        output, memory, _ = decoder(
            decoder_input, memory, encoder_outputs)

        _, topi = output.topk(1)
        decoder_input = topi.squeeze().detach()

        loss += loss_fn(output, target_tensor[i])
        if decoder_input.item() == EOS_TOKEN:
            break

    loss.backward()

    encoder_optimizer.step()
    decoder_optimizer.step()

    return loss.item() / target_tensor.size(0)


def train_iters(encoder: Encoder, decoder: Decoder, train_set, src_lang, tgt_lang, lr=0.1):
    NUM_INTERVALS = 20
    total_loss = 0

    encoder_optimizer = SGD(encoder.parameters(), lr=lr)
    decoder_optimizer = SGD(decoder.parameters(), lr=lr)
    loss_fn = CrossEntropyLoss()

    train_len = len(train_set)
    for i in range(train_len):
        input_tensor = train_set[i][src_lang]
        target_tensor = train_set[i][tgt_lang]

        loss = train(input_tensor, target_tensor, encoder, decoder,
                     encoder_optimizer, decoder_optimizer, loss_fn)


def train_model(model, train, src_lang, tgt_lang):
    """
    Trains seq2seq RNN model.

    :param encoder: Encoder
    :param decoder: Decoder
    :param train: training set
    :lr: learning rate
    """

    train_iters(model["encoder"], model["decoder"], train, src_lang, tgt_lang)


def translate(string, encoder, decoder, src_lang, tgt_lang):
    with no_grad():
        norm_msg = normalize(string, src_lang)
        str_tensor = convert_to_tensor(norm_msg, src_lang)
        memory = encoder.init_memory()

        encoder_outputs = zeros(
            decoder.max_len, encoder.memory_size, device=DEVICE)

        for i in range(str_tensor.size(0)):
            print(str_tensor[i])
            output, memory = encoder(str_tensor[i], memory)
            encoder_outputs[i] = output[0, 0]

        translated_words = []

        decoder_input = tensor([[SOS_TOKEN]], device=DEVICE)
        for i in range(decoder.max_len):
            output, memory, _ = decoder(
                decoder_input, memory, encoder_outputs)

            _, topi = output.topk(1)

            if topi.item() == EOS_TOKEN:
                break
            else:
                translated_words.append(
                    vocab[tgt_lang].index2word[topi.item()])

            decoder_input = topi.squeeze().detach()

        return translated_words


def init_model():
    print("initializing machine translation models...")

    global tokenizer
    tokenizer = {
        "en": load("en_core_web_sm"),
        "es": load("es_core_news_sm"),
    }

    dataset = load_dataset(DATASET_FILE, SRC_LANG, TGT_LANG)

    global vocab
    vocab = create_vocabs(dataset)

    train, test = get_train_test(dataset)

    MEM_SIZE = 256
    en2es = {
        "encoder": Encoder(vocab[SRC_LANG].num_words, MEM_SIZE).to(DEVICE),
        "decoder": Decoder(vocab[TGT_LANG].num_words, MEM_SIZE, max_len=max_length).to(DEVICE)
    }
    es2en = {
        "encoder": Encoder(vocab[TGT_LANG].num_words, MEM_SIZE).to(DEVICE),
        "decoder": Decoder(vocab[SRC_LANG].num_words, MEM_SIZE, max_len=max_length).to(DEVICE)
    }

    global translator
    translator = {
        "en": {"es": en2es},
        "es": {"en": es2en}
    }

    print("training models...")
    train_model(en2es, train, SRC_LANG, TGT_LANG)
    train_model(es2en, train, TGT_LANG, SRC_LANG)


def get_translator(src_lang, tgt_lang):
    return translator[src_lang][tgt_lang]["encoder"], translator[src_lang][tgt_lang]["decoder"]
