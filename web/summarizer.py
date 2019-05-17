from nltk.tokenize import sent_tokenize
from nltk import word_tokenize
import lemmagen
from lemmagen.lemmatizer import Lemmatizer

only_word = lambda s: ''.join([i for i in s if i.isalnum()])
language_switcher = {
        'en': lemmagen.DICTIONARY_ENGLISH,
        'rs': lemmagen.DICTIONARY_SERBIAN,
        'it': lemmagen.DICTIONARY_ITALIAN,
        'fr': lemmagen.DICTIONARY_FRENCH,
        'de': lemmagen.DICTIONARY_GERMAN,
        'es': lemmagen.DICTIONARY_SPANISH,
        'cz': lemmagen.DICTIONARY_CZECH,
        'bg': lemmagen.DICTIONARY_BULGARIAN,
        'ee': lemmagen.DICTIONARY_ESTONIAN,
    }


def summarize(text, numSentences, method='sum', lang='si'):
    global only_word, language_switcher
    l = Lemmatizer(dictionary=language_switcher.get(lang, lemmagen.DICTIONARY_SLOVENE))
    a = bytes(text, 'utf-8').decode('utf-8','ignore')
    sentences = sent_tokenize(a)
    words = []
    allWords = {} # holds frequencies of all words in the text

    for s in sentences:
        words.append([])
        for i in word_tokenize(s):
            temp = only_word(i).lower()
            if len(temp) > 0:
                temp = l.lemmatize(temp)
                words[-1].append(temp)
                if temp not in allWords:
                    allWords[temp] = 1
                else:
                    allWords[temp] += 1


    def dictSum(wordList):
        # returns "weight" (sum) of a sentence based on the list of words 
        ret = 0
        for i in wordList:
            ret += allWords[i]
        return ret

    if method == 'sum': weights = [dictSum(words[i]) for i in range(len(sentences))]
    else: weights = [dictSum(words[i])/len(words[i]) for i in range(len(sentences))] # method == 'average'

    w2 = weights.copy()
    w2.sort(reverse=True)

    if numSentences > len(w2): numSentences = len(w2)
    mborder = w2[numSentences-1]
    out = ''
    for i, s in enumerate(sentences):
        if weights[i] >= mborder: out += s.replace('\n','') + ' '

    return out
