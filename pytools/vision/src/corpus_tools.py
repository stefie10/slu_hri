from nltk.corpus import gutenberg


def match_sentences(corp, wordlist):
    sentences = corp.sents()

    ret_sents = {}
    for sentence in sentences:
        for word in sentence:
            if(word in wordlist):
                try:
                    ret_sents[word].append(sentence)
                except:
                    ret_sents[word] = []
                    ret_sents[word].append(sentence)
    return ret_sents


def create_prob_dist(corp, wordlist):

    #match elements of the object list to the corpus
    sents = match_sentences(corp, wordlist)

    #initialize
    counts = {}
    for k in sents.keys():
        counts[k] = {}

    #count the occurrances
    for k in sents.keys():
        ss = sents[k]

        for s in ss:
            for w in s:
                try:
                    counts[k][w]+=1
                except:
                    counts[k][w]=1

    #print
    for k in counts.keys():
        print k, "-->", counts[k]
        raw_input()



if __name__=="__main__":

    myfile = open("object_list.txt")

    wordlist = []
    for line in myfile:
        wordlist.append(line.split()[0])

    #print wordlist
    #raw_input()
    print "matching sentences"
    create_prob_dist(gutenberg, wordlist)


