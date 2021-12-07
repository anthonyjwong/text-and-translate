from random import shuffle

from spacy import load
from torch import device, long, tensor, zeros
from torch.cuda import is_available as cuda_is_available
from torch.nn.modules.loss import NLLLoss
from torch.optim import SGD

from nlp.rnn import Decoder, Encoder
from nlp.vocab import EOS_TOKEN, SOS_TOKEN, Vocab

DEVICE = device("cuda" if cuda_is_available() else "cpu")


DATASET_FILE = "nlp/tatoeba.txt"
LANGS = ["en", "es"]
SRC_LANG = "en"
TGT_LANG = "es"
MAX_TRAIN_SIZE = 1000


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
    dataset = []
    with open(filename, "r") as file:
        datum = file.readline()
        i = 0
        while i < MAX_TRAIN_SIZE and datum:
            datum = datum.split('\t')
            dataset.append({
                src_lang: normalize(datum[0]),
                tgt_lang: normalize(datum[1])
            })

            datum = file.readline()
    return dataset


def normalize(string, lang):
    """
    Normalizes string. Proper nouns stay capitalized.

    :param string: string to normalize
    :param lang: language of string
    :return: string
    """
    doc = tokenizer[lang](string)
    string = [token.text.lower() if token.pos_ !=
              "PROPN" else token.text for token in doc]
    return " ".join(string)


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
    indices = [vocab[lang].word2index[word] for word in string]
    indices.append(EOS_TOKEN)

    return tensor(indices, dtype=long,
                  device=DEVICE).view(-1, 1)


def convert_to_tensors(dataset):
    """
    Converts dataset to tensor for model input.

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
    dataset = convert_to_tensors(dataset)

    shuffle(dataset)    # shuffles in place
    train_test_split = split * len(dataset)
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
        output, memory = encoder(input_tensor[0], memory)
        encoder_outputs[i] = output[0, 0]

    decoder_input = tensor([[SOS_TOKEN]], device=DEVICE)
    for i in range(target_tensor.size(0)):
        output, memory, attn = decoder(decoder_input, memory, encoder)

        topv, topi = output.topk(1)
        decoder_input = topi.squeeze().detach()

        loss += loss_fn(output, target_tensor[i])
        if decoder_input.item() == EOS_TOKEN:
            break

    loss.backward()

    encoder_optimizer.step()
    decoder_optimizer.step()

    return loss.item() / target_tensor.size(0)


def train_iters(encoder: Encoder, decoder: Decoder, train, src_lang, tgt_lang, lr=0.01):
    total_loss = 0

    encoder_optimizer = SGD(encoder.parameters(), lr=lr)
    decoder_optimizer = SGD(decoder.parameters(), lr=lr)
    loss_fn = NLLLoss()

    for i in range(len(train)):
        input_tensor = train[i][src_lang]
        target_tensor = train[i][tgt_lang]

        loss = train(input_tensor, target_tensor, encoder, decoder,
                     encoder_optimizer, decoder_optimizer, loss_fn)

        if i % 10 == 0:
            total_loss += loss
            print(f"{(i / len(train)) * 100}%, AVG LOSS: {total_loss / i}")


def train_model(model, train, src_lang, tgt_lang):
    """
    Trains seq2seq RNN model.

    :param encoder: Encoder
    :param decoder: Decoder
    :param train: training set
    :lr: learning rate
    """

    train_iters(model["encoder"], model["decoder"], train, src_lang, tgt_lang)


def init_model():
    global tokenizer
    tokenizer = {
        "en": load("en_core_web_sm"),
        "es": load("es_core_news_sm"),
    }
    dataset = load_dataset(DATASET_FILE)

    global vocab
    vocab = create_vocabs(dataset)

    train, test = get_train_test(dataset)

    MEM_SIZE = 256
    en2es = {
        "encoder": Encoder(vocab[SRC_LANG].num_words, MEM_SIZE).to(device),
        "decoder": Decoder(vocab[TGT_LANG].num_words, MEM_SIZE)
    }
    es2en = {
        "encoder": Encoder(vocab[TGT_LANG].num_words, MEM_SIZE).to(device),
        "decoder": Decoder(vocab[SRC_LANG].num_words, MEM_SIZE)
    }

    train_model(en2es, train, SRC_LANG, TGT_LANG)
    train_model(es2en, train, TGT_LANG, SRC_LANG)
