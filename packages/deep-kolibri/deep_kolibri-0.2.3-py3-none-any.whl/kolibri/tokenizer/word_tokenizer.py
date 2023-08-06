
from kolibri.document import Document
from kolibri.tokenizer import RegexpTokenizer
from kolibri.tokenizer.tokenizer import Tokenizer
from kolibri.stopwords import get_stop_words
pattern = r'\b(?:[A-Z][@\.A-Z-]{2,}|[\w-]{2,}|(?:\d+(?:[\.,:]\d+)*))\b'

tknzr=RegexpTokenizer(pattern)


class WordTokenizer(Tokenizer):
    name = "word_tokenizer"

    provides = ["tokens"]
    defaults = {
        "remove-stopwords": True,
        "language": 'en',
        "lower-case": False
    }

    def __init__(self, config={}):
        super().__init__(config)
        self.stopwords=None
        self.remove_stopwords=self.component_config["remove-stopwords"]
        if self.remove_stopwords    :
            self.stopwords=get_stop_words(self.component_config['language'])

    def fit(self, training_data, target):
        return self

    def transform(self, data, **kwargs):
        if self.remove_stopwords:
            if not self.component_config['lower-case']:
                return [[w for w in tknzr.tokenize(d) if w not in self.stopwords] for d in data]
            else:
                return [[w.lower() for w in tknzr.tokenize(d) if w.lower() not in self.stopwords] for d in data]

        else:
            return [tknzr.tokenize(d) for d in data]

    def process(self, document:Document, **kwargs):
        if hasattr(document, '_sentences'):
            document.tokens=[]
            for sentence in document.sentences:
                if self.remove_stopwords:
                    document.tokens.append([ w for w in tknzr.tokenize(sentence) if w not in self.stopwords])
                else:
                    document.tokens.append(tknzr.tokenize(sentence))
            document.sentences=None
        else:
            if self.remove_stopwords:
                document.tokens=[ w for w in tknzr.tokenize(document.text) if w not in self.stopwords]
            else:
                document.tokens = tknzr.tokenize(document.text)
            document.raw_text=None

    def get_info(self):
        return "word_tokenizer"