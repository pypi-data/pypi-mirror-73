from soynlp.hangle import decompose, compose
import re

class Utility:
    def __init__(self):
        name = 'Utility Class'
        self.doublespace_pattern = re.compile('\s+')

    def jamo_sentence(self, sent):

        def transform(char):
            if char == ' ':
                return char
            cjj = decompose(char)
            if len(cjj) == 1:
                return cjj
            cjj_ = ''.join(c if c != ' ' else '-' for c in cjj)
            return cjj_

        sent_ = ''.join(transform(char) for char in sent)
        sent_ = self.doublespace_pattern.sub(' ', sent_)
        return sent_

    def decode(self, s):
        def process(t):
            assert len(t) % 3 == 0
            t_ = t.replace('-', ' ')
            chars = [tuple(t_[3 * i:3 * (i + 1)]) for i in range(len(t_) // 3)]
            recovered = [compose(*char) for char in chars]
            recovered = ''.join(recovered)
            return recovered

        return ' '.join(process(t) for t in s.split())

    def decode_sentence(self, sent):
        return ' '.join(self.decode(token) for token in sent.split())