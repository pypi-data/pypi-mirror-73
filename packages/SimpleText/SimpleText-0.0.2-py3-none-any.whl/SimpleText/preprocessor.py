# import libararies

import re
import string
import unicodedata
import nltk
from nltk import ngrams
from nltk.tokenize import sent_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.stem.porter import PorterStemmer

nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)
nltk.download('wordnet', quiet=True)

stop_words = list(stopwords.words('english'))


# define functions 

def strip_accents(text):
    """This function strips accents from strings.

    Input:
    text (string): A text string

    Returns:
    text (string): text without accents
    """
    try:
        text = unicode(text, 'utf-8')
    except NameError:
        pass

    text = unicodedata.normalize('NFD', text).encode('ascii', 'ignore').decode("utf-8")

    return str(text)


def get_ngrams(text, n_grams):
    """Takes text and returns a list of the ngrams

    Parameters:
    text (string): a string of text
    n_grams (tuple): specifies the number of ngrams e.g. (1,2) would be unigrams
                     and bigrams, (1,1) would be unigrams.

    Returns:
    ngrams_list(list): a list of the ngrams
    """
    ngrams_list = []
    for n in range(n_grams[0], n_grams[1]+1):
        if n <= 1:
            pass
        else:
            sentances = sent_tokenize(text)
            for sent in sentances:
                grams = ngrams(sent.split(), n)
                for gram in grams:
                    ngrams_list.append(gram)

    return ngrams_list


def preprocess(text, n_grams=(1, 1), remove_accents=False, lower=False, remove_less_than=0,
               remove_more_than=20, remove_punct=False, remove_alpha=False, remove_stopwords=False,
               remove_custom_stopwords=[], lemma=False, stem=False, remove_url=False):
    """Takes text and outputs a pre-processed list of tokens.

    Parameters:
    text (string): a string of text
    n_grams (tuple): specifies the number of ngrams e.g. (1,2) would be unigrams and bigrams,
                     (1,1) would be unigrams
    remove_accents (boolean): removes accents
    lower (boolean): lowercases text
    remove_less_than (int): removes words less than X letters
    remove_more_than (int): removes words more than X letters
    remove_punct (boolean): removes punctuation
    remove_alpha (boolean): removes non-alphabetic tokens
    remove_stopwords (boolean): removes stopwords
    remove_custom_stopwords (list): removes custom stopwords
    lemma (boolean): lemmantises tokens (via the Word Net Lemmantizer algorithm)
    stem (boolean): stems tokens (via the Porter Stemming algorithm)

    Returns:
    tokens (list): a list of cleaned tokens
    """

    if remove_custom_stopwords is None:
        remove_custom_stopwords = []
        
    if lower is True:
        text = text.lower()

    if remove_accents is True:
        text = strip_accents(text)

    if remove_punct is True:
        text = text.rstrip().translate(str.maketrans('', '', string.punctuation))

    if remove_url is True:
        text = re.sub(r"http\S+", '', text )

    tokens = text.split()

    if remove_alpha is True:
        tokens = [token for token in tokens if token.isalpha()]

    if remove_stopwords is True:
        tokens = list(set(tokens) - set(stop_words))

    if len(remove_custom_stopwords) > 0:
        tokens = list(set(tokens) - set(remove_custom_stopwords))

    if lemma is True:
        tokens = [WordNetLemmatizer().lemmatize(token) for token in tokens]

    if stem is True:
        tokens = [PorterStemmer().stem(token) for token in tokens]

    ngrams_list = get_ngrams(text, n_grams)

    return tokens + ngrams_list
