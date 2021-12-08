from nltk import sent_tokenize, word_tokenize

SOS_TOKEN = 0
EOS_TOKEN = 1


class Vocab:
    def __init__(self, data_iter, lang):
        self.lang = lang
        self.word2index = {}
        self.index2word = {0: "SOS", 1: "EOS"}
        self.word_freq = {}
        self.num_words = 2

        for datum in data_iter:
            sents = sent_tokenize(datum)
            for sent in sents:
                words = word_tokenize(sent)
                for word in words:
                    self.add_word(word)

    def add_word(self, word):
        if word not in self.word2index:
            self.word2index[word] = self.num_words
            self.index2word[self.num_words] = word
            self.num_words += 1
            self.word_freq[word] = 1
        else:
            self.word_freq[word] += 1

        return self.word2index[word]
