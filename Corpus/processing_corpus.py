import nltk, string
from nltk import FreqDist
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
    
def setupCorpus():
    fileHandler = open('D:/awi/Documents/UNI/AI Master Sem 2/NLP/python/hundred_K.txt',encoding='utf-8')
    corpus = fileHandler.read()
    tokens = word_tokenize(corpus)
    stop_Token = stopwords.words("english") + list(string.punctuation) # this is the stop words like punctuation and all - suggested to be removed 

    filteredTokens = []
    for word in tokens:
        if word not in stop_Token:
            filteredTokens.append(word)
    repeated_words = []
    tokens1 = []
    [tokens1.append(word) for word in tokens if word not in tokens1]

    print("\nThere are ",len(corpus), len(tokens), "words in this text","\nThere are ", len(filteredTokens),len(tokens1), "words in this text after removing stop words\n")#,filteredTokens)
    allwords = FreqDist(filteredTokens)
    print(allwords.most_common(15))


setupCorpus()