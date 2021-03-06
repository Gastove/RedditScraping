import csv
import os
import gensim
import nltk
import logging

in_dir = '/Users/mlinegar/Data/LDA/Usertext/'
out_dir = '/Users/mlinegar/Data/LDA/textfiles/'
processed_dir = 'Users/mlinegar/Data/LDA/BoW'

for user in os.listdir(in_dir):
    with open(in_dir + user, 'r') as f:
        rdr = csv.reader(f)
        print("Converting User: %s"  %user)
        firstcolumn = [row[0] for row in rdr]

    with open(out_dir + user + '.txt', 'w') as textfile:
        textfile.writelines(firstcolumn)

def iter_docs(topdir, stoplist):
    for user in os.listdir(topdir):
        with open(os.path.join(topdir, user), 'rbRight') as g:
            text = g.read()
            yield(x for x in gensim.utils.tokenize(text, lowercase= True, deacc= True, errors= "ignore")
            if x not in stoplist)

class MyCorpus(object):
    def __init__(self, topdir, stoplist):
        self.topdir = topdir
        self.stoplist = stoplist
        self.dictionary = gensim.corpora.Dictionary(iter_docs(topdir, stoplist))

    def __iter__(self):
        for tokens in iter_docs(self.topdir, self.stoplist):
            yield self.dictionary.doc2bow(tokens)

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s',
                    level=logging.INFO)

stoplist = set(nltk.corpus.stopwords.words("english"))
corpus = MyCorpus(out_dir, stoplist)

corpus.dictionary.save(os.path.join(processed_dir, "firsttry.dict"))
gensim.corpora.MmCorpus.serialize(os.path.join(processed_dir, "firsttry.mm"), corpus)

# I think the problem is a problem with Pickle - Pickle expects us to use 'rb', here we use just 'r'.