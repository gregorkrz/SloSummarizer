from nltk.tokenize import sent_tokenize
from nltk import word_tokenize
from lemmagen.lemmatizer import Lemmatizer

l = Lemmatizer()
only_word = lambda s: ''.join([i for i in s if i.isalnum()])

def summarize(text, numSentences):
    global l, only_word
    
    a = bytes(text, 'utf-8').decode('utf-8','ignore')
    sentences = sent_tokenize(a)
    words = []
    allWords = {} # holds frequencies of all words in the text

    for s in sentences:
        words.append([])
        for i in word_tokenize(s):
            temp = only_word(i).upper()
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

    weights = [dictSum(words[i]) for i in range(len(sentences))]

    w2 = weights.copy()
    w2.sort(reverse=True)

    if numSentences > len(w2): numSentences = len(w2)
    mborder = w2[numSentences-1]
    out = ''
    for i, s in enumerate(sentences):
        if weights[i] >= mborder: out += s.replace('\n','') + ' '

    return out
