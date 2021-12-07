from torch import bmm, cat, zeros
from torch.cuda import memory
from torch.nn import GRU, Dropout, Embedding, Linear, Module
from torch.nn.functional import log_softmax, relu, softmax

from nlp.model import DEVICE


class Encoder(Module):
    def __init__(self, input_size, memory_size):
        super(Encoder, self).__init__()
        self.memory_size = memory_size

        self.embedding = Embedding(input_size, memory_size)
        self.gru = GRU(memory_size, memory_size)

    def forward(self, input, memory):
        output = self.embedding(input).view(1, 1, -1)
        return self.gru(output, memory)

    def init_memory(self):
        return zeros(1, 1, self.memory_size, device=DEVICE)


class Decoder(Module):
    def __init__(self, output_size, memory_size, dropout=0.1, max_len=50):
        super(Encoder, self).__init__()
        self.max_len = max_len

        self.memory_size = memory_size

        self.embedding = Embedding(output_size, memory_size)
        self.dropout = Dropout(dropout)

        self.attn = Linear(memory_size * 2, max_len)
        self.attn_combine = Linear(memory_size * 2, memory_size)

        self.gru = GRU(memory_size, memory_size)
        self.output = Linear(memory_size, output_size)

    def forward(self, input, memory, encoder_outputs):
        output = self.embedding(input).view(1, 1, -1)
        output = self.dropout(output)

        # calculate attn weights
        attn_weights = softmax(
            self.attn(cat((output[0], memory[0]), 1)), dim=1)
        attn_applied = bmm(attn_weights.unsqueeze(0),
                           encoder_outputs.unsqueeze(0))

        # apply attn weights
        output = cat((output[0], attn_applied[0]), 1)
        output = self.attn_combine(output).unsqueeze(0)

        output = relu(output)
        output, memory = self.gru(output, memory)

        output = log_softmax(self.output(output[0]), dim=1)

        return output, memory, attn_weights

    def init_memory(self):
        return zeros(1, 1, self.memory_size, device=DEVICE)
