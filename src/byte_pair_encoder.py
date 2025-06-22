import re
import collections


class BytePairEncoder:
    def __init__(self):
        self.merges = None
        self.characters = None
        self.tokens = None
        self.vocab = None

    def format_word(self, text, space_token='_'):
        return ' '.join(list(text)) + ' ' + space_token

    def initialize_vocab(self, text):
        text = re.sub('\s+', ' ', text)
        all_words = text.split()
        vocab = {}
        for word in all_words:
            word = self.format_word(word)
            vocab[word] = vocab.get(word, 0) + 1  # count occurrences of each word
        tokens = collections.Counter(text) # calculate the count of each element in the iterable
        return vocab, tokens

    def get_bigram_counts(self, vocab):
        pairs = {}
        for word, count in vocab.items():
            symbols = word.split()
            for i in range(len(symbols)-1):
                pair = (symbols[i], symbols[i+1])
                pairs[pair] = pairs.get(pair, 0) + count
        return pairs

    def merge_vocab(self, pair, vocab_in):
        vocab_out = {}
        bigram = re.escape(' '.join(pair))
        # here define a regex pattern in a way , there should be only a whitespace before and after the bigram , making it as a seperate word
        p = re.compile(r'(?<!\S)' + bigram + r'(?!\S)')
        bytepair = ''.join(pair)
        for word in vocab_in:
            w_out = p.sub(bytepair, word)
            vocab_out[w_out] = vocab_in[word]
        return vocab_out, (bigram, bytepair)
 
    def find_merges(self, vocab, tokens, num_merges):
        merges = []
        for i in range(num_merges):
            # bigram counts
            pairs = self.get_bigram_counts(vocab)
            # bigram pair with highest frequency 
            best_pair = max(pairs, key=pairs.get)
            best_count = pairs[best_pair]

            vocab, (bigram, bytepair) = self.merge_vocab(best_pair, vocab)
            merges.append((r'(?<!\S)' + bigram + r'(?!\S)', bytepair))
            tokens[bytepair] = best_count
        return vocab, tokens, merges

    def fit(self, text, num_merges):
        # vocab : holds the words frequency 
        # token : holds the frequency of each character  
        vocab, tokens = self.initialize_vocab(text)  # vocab ->  {word: count}, tokens -> {char: count}
        self.characters = set(tokens.keys()) # chars present in the tokens
        self.vocab, self.tokens, self.merges = self.find_merges(vocab, tokens, num_merges)

    @property
    def get_tokens(self):
        return self.tokens

    @property
    def get_characters(self):
        return self.characters
