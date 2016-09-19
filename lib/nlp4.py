import numpy as np
import pandas as pd
from collections import defaultdict
import math as math
import nltk
from nltk import corpus
from nltk import classify

from nltk.classify.api import ClassifierI, MultiClassifierI
from nltk.classify.megam import config_megam, call_megam
from nltk.classify.weka import WekaClassifier, config_weka
from nltk.classify.naivebayes import NaiveBayesClassifier
from nltk.classify.positivenaivebayes import PositiveNaiveBayesClassifier
from nltk.classify.decisiontree import DecisionTreeClassifier
from nltk.classify.rte_classify import rte_classifier, rte_features, RTEFeatureExtractor
from nltk.classify.util import accuracy, apply_features, log_likelihood
from nltk.classify.scikitlearn import SklearnClassifier
from nltk.classify.maxent import (MaxentClassifier, BinaryMaxentFeatureEncoding,
                                  TypedMaxentFeatureEncoding,
                                  ConditionalExponentialClassifier)
from nltk.tag.crf import CRFTagger
from sklearn.preprocessing import LabelBinarizer
from itertools import chain
from sklearn.metrics import classification_report, confusion_matrix
import re
from HTMLParser import HTMLParser
from sklearn.cross_validation import train_test_split


# each tweet is loaded as a paragraph in a single document corpus.
prodCorpus=corpus.TaggedCorpusReader('./data.train/', 'train.txt', '\t')
trainCorpus=corpus.TaggedCorpusReader('./data.dev/', 'train.txt', '\t')
evalCorpus=corpus.TaggedCorpusReader('./data.dev/', 'dev1.txt', '\t')
testCorpus=corpus.TaggedCorpusReader('./data.train/', 'TestNoLabels.txt', '\t')
tweet=trainCorpus.paras()[0]
print "loaded all: sample", tweet


class Annotation:
    def __init__(self, text, annoType, doc=None, tStart=0, tEnd=0, cStart=0, cEnd=0 ):
        self.features={}
        self.labels=[]
        self.tStart=tStart
        self.tEnd=tEnd
        self.cStart=cStart
        self.cEnd=cEnd
        self.text=text
        self.annoType=annoType
        self.doc=doc

    def getText(self):
        return self.text

    def addFeature(self, fname, fval):
        self.features[fname]=fval

    def getFeatures(self):
        return self.features

    def addLabel(self,label):
        self.labels.append(label)

    def setLabel(self,lbl_idx, label):
        self.labels[lbl_idx]=label

    def getLabels(self):
        return self.labels

    def __str__(self):
        return self.getText()

    def __repr__(self):
        return self.text + '//tkn idx'+str(self.tStart)+":"+str(self.tEnd)



class Document:
    '''Documents can handle token level, sentence level and span level annotations.'''
    items={}
    def __init__(self, src, srcType='Token'):
#       srcType can be Raw, Sent, Word/Token
        self.src=src

        if(srcType=='Token'):
            self.src=src
            # for list type Token
            self.tokens=[]
            text=""
            for t in self.src:
                tText=t[0].encode('utf-8')
                tkn=Annotation(tText,'Token', self)
                if len(t)>1:
                    tkn.addLabel(t[1])
                else:
                    tkn.addLabel('NA')
                self.tokens.append(tkn)
                text=text+" "+tText
            self.text=text
            self.sents=None


        elif (srcType=='Raw'):
            self.tokens=[]
            self.sents=[]
            if type(src)==str:
                self.text=src.decode('utf-8')
            else:
                self.text=src.decode('utf-8')

        self.docFeatures={}
        self.items['raw']=src
        self.items['doc-features']=self.docFeatures
        self.items['tokens']=self.tokens
        self.items['sents']=self.sents

    def addAnnotationSet(self, annType, annots):
        '''@annType is the annotation type. ex: Entity.
           @annots are a list of annotations'''
        self.items[annType]= annots

    def getRaw(self):
        return self.src

    def getText(self):
        return self.text

    def getSents(self):
        return self.sents

    def getTokens(self):
        return self.tokens;

    def setTokens(self, tokens):
        self.tokens=tokens

    def setSents(self, sents):
        self.sents=sents

    def getAnnotation(start, end):
        '''return the annotation spanning the tokens indexed by start and end token
            @param start= start token id
            @param end  = end token id
        '''
        pass

    def getTokenLabelSets(self):
        return [t.labels for t in self.tokens]

    def getTokenLabelsAt(self, idx):
        return [t.labels[idx] for t in self.tokens]

    def getSentLabelSets(self):
        return [s.labels for s in self.sents]

    def getSentLabelsAt(self, idx):
        return [s.labels[idx] for s in self.sents]

    def addTokenFeature(self, i,fname, fval):
        self.tokens[i].features[fname]=fval

    def getTokenFeatures(self, i):
        '''get feature set for token i'''
        return self.tokens[i].features

    def getTokenFeatureSets(self):
        return [t.features for t in self.tokens]

    def addSentFeature(self, i, fname, fval ):
        self.sentFeatures[i][fname]=fval

    def getSentFeatures(self, i):
        '''get feature set for token i'''
        return self.sents[i].features

    def getSentFeatureSets(self):
        return [s.features for s in self.sents]

    def addSentFeature(self, i, fname, fval ):
        self.sents[i].features[fname]=fval

    def addDocFeature(self, fname, fval ):
        self.docFeatures[fname]=fval

    def getDocFeature(self, fname ):
        return self.docFeatures[fname]

    def __getitem__(self, key):
        return self.items[key]

    def __setitem__(self,key,value):
        self.items[key]=value

    def __missing__(self,key):
        if(key=="token-labels"):
            return self.getTokenLabels()
    def __str__(self):
        return self.getText()

    def __repr__(self):
        return "text:"+self.getText()+" //tknf"+str(self.getTokenFeatures(0))





prod_tweets=[]
train_tweets=[]
eval_tweets=[]
test_tweets=[]
def extractTweets(corpus, toList):
    for tweet in corpus.paras():
        toList.append(Document(tweet))

extractTweets(prodCorpus, prod_tweets)
extractTweets(trainCorpus, train_tweets)
extractTweets(evalCorpus, eval_tweets)
extractTweets(testCorpus, test_tweets)
print prod_tweets[0]
print train_tweets[1]
print eval_tweets[0]
print test_tweets[0]


## Arc pos tagger
import arktweetnlp as ark
reload(ark.CMUTweetTagger)
def getArcPosTags(tweets):
    tweets_str=[str(t) for t in tweets]
    ark_tagged=ark.CMUTweetTagger.runtagger_parse(tweets_str)
    return ark_tagged


## GATE Twittie tagger
import twitietagger as twt
# reload(twt.TwitieTagger)
def getTwitiePosTags(tweets):
    twitie_tagged=twt.TwitieTagger.parse(tweets)
    return twitie_tagged


def getNLTKTags(tweets):
    nltkTagged=[]
    for t in tweets:
        tweet=t.getText().decode('utf-8').encode('ascii' , 'replace')
        tagged=nltk.pos_tag(nltk.word_tokenize(tweet))
        nltkTagged.append(tagged)
    return nltkTagged

prod_pos=getNLTKTags(prod_tweets)
train_pos=getNLTKTags(train_tweets)
eval_pos=getNLTKTags(eval_tweets)
test_pos=getNLTKTags(test_tweets)



# get the tagged
prod_ark=getArcPosTags(prod_tweets)
train_ark=getArcPosTags(train_tweets)
eval_ark=getArcPosTags(eval_tweets)
test_ark=getArcPosTags(test_tweets)

prod_twitie=getTwitiePosTags(prod_tweets)
print len(prod_twitie)
train_twitie=getTwitiePosTags(train_tweets)
print len(train_twitie)
eval_twitie=getTwitiePosTags(eval_tweets)
print len(eval_twitie)
test_twitie=getTwitiePosTags(test_tweets)
print len(test_twitie)


print 'check lengths of tagged and orignal are eq'
print len(prod_tweets)
print len(prod_twitie)
print len(prod_ark)
print len(train_tweets)
print len(train_twitie)
print len(train_ark)
print len(eval_tweets)
print len(eval_twitie)
print len(eval_ark)

print len(test_tweets)
print len(test_twitie)
print len(test_ark)


# Aligning Tokens
h = HTMLParser()
def mergeTokens(tokens, tags):
    if len(tokens) != len(tags):
        newTags=[]
        j=0
        for i,tkn in enumerate(tokens):
            word=h.unescape(tkn.getText())
            word2=h.unescape(tags[j][0])
            if word2==word:
                newTags.append((tags[j][0],tags[j][1]))
                j+=1
            elif len(word) > len(word2):
#                 print word, word2
                comb=[(tags[j][0], tags[j][1])]
                word3=word2
                while len(word)> len(word3):
                    j+=1
                    word3+=h.unescape(tags[j][0])
                    comb.append((tags[j][0], tags[j][1]))

                mergedWord=""
                mergedTag=""
                for tag in comb:
                    mergedWord+=tag[0]
                    mergedTag=tag[1]  #lets keep last one's tag
                newTags.append((mergedWord, mergedTag))
                j+=1
            else:
                newTags.append((word,tags[j][1]))
                j+=1
#                 print word, word2
        return newTags
    else:
        return tags

n=0
tokens=prod_tweets[n].getTokens()
merged= mergeTokens(tokens, prod_ark[n])
print 'tweet:', prod_tweets[n]
print 'ark t:', prod_ark[n]
print 'merged', merged
# print prod_twitie[n]

print len(merged), len(tokens)



##Add POS types as features
def addPOSFeatures(tweets, ark_tags , twitie_tags, nltk_tags):
#     print len(tweets)
#     print len(ark_tags)
#     print len(twitie_tags)
    for i,doc in enumerate(tweets):
#         print i
        tokens=doc.getTokens()
        tTags=mergeTokens(tokens, twitie_tags[i])
        aTags= ark_tags[i]  #rm
        nTags=nltk_tags[i]
        for j, tkn in enumerate(tokens):
            f=tkn.getFeatures()
            f['TPOS']=tTags[j][1]
            f['APOS']=aTags[j][1]
            f['NPOS']=nTags[j][1]


# all_tweets[0].getTokenFeatureSets()
addPOSFeatures(prod_tweets, prod_ark, prod_twitie, prod_pos )
addPOSFeatures(train_tweets, train_ark, train_twitie, train_pos)
addPOSFeatures(eval_tweets, eval_ark, eval_twitie, eval_pos)
addPOSFeatures(test_tweets, test_ark, test_twitie, test_pos)

print prod_tweets[0]
print train_tweets[1]
print eval_tweets[0]
print prod_ark[0]
print prod_twitie[0]
prod_tweets[0].getTokenFeatures(0)

##############################
#### DEPENDANCY PARSING ######
##############################

###Prepare tweet input files for parsing. Parsed output files are in data.parsed
### pre parsed the data offline since TweeboParser needs  C++ dependancies like cmake and needs to be installed to run.

# def writeToFile(tweets, filename):
#     inFile= open(filename, 'w')
#     for tweet in tweets:
#         inFile.write("%s\n" % tweet.getText())
#     inFile.close()

# writeToFile(prod_tweets, 'prodTweets.txt')
# writeToFile(train_tweets, 'trainTweets.txt')
# writeToFile(eval_tweets, 'evalTweets.txt')
# writeToFile(test_tweets, 'testTweets.txt')

WORDS = 'words'   #: column type for words
POS = 'pos'       #: column type for part-of-speech tags
TREE = 'tree'     #: column type for parse trees
CHUNK = 'chunk'   #: column type for chunk structures
NE = 'ne'         #: column type for named entities
SRL = 'srl'       #: column type for semantic role labels
IGNORE = 'ignore' #: column type for column that should be ignored

# 1       OMG     _       !       !       _       0       _
# 2       I       _       O       O       _       6       _
# 3       ♥       _       V       V       _       6       CONJ

# ctypes={TREE, WORDS,  IGNORE, POS, POS, IGNORE, TREE, POS}

prod_parse=corpus.TaggedCorpusReader('./data.parsed/', 'prodTweets.txt.predict', '\t')
train_parse=corpus.TaggedCorpusReader('./data.parsed/', 'trainTweets.txt.predict', '\t')
eval_parse=corpus.TaggedCorpusReader('./data.parsed/', 'evalTweets.txt.predict', '\t')
test_parse=corpus.TaggedCorpusReader('./data.parsed/', 'testTweets.txt.predict', '\t')

prod_deps=[ dep for dep in prod_parse.paras()]
train_deps=[ dep for dep in train_parse.paras()]
eval_deps=[ dep for dep in eval_parse.paras()]
test_deps=[ dep for dep in test_parse.paras()]

print len(prod_deps), len(prod_tweets)
print len(train_deps), len(train_tweets)
print len(eval_deps), len(eval_tweets)
print len(test_deps), len(test_tweets)


def alignDepGraph(docs, depTagSets):
    aligned=[]
    for i,doc in enumerate(docs):
        aligned.append(__alignDepGraph(doc.getTokens(), depTagSets[i]))
    return aligned


h = HTMLParser()
def __alignDepGraph(tokens, tags):
    if len(tokens) != len(tags):
        newTags=[]
        j=0
        for i,tkn in enumerate(tokens):
            word=h.unescape(tkn.getText())
            word2=h.unescape(tags[j][1])
            if word2==word:
                newTags.append((tags[j][0],tags[j][1], tags[j][3], tags[j][-2], tags[j][-1]))
                j+=1
            elif len(word) > len(word2):
#                 print word, word2
                comb=[(tags[j][0], tags[j][1], tags[j][3], tags[j][-2], tags[j][-1])]
                word3=word2
                while len(word)> len(word3):
                    j+=1
                    word3+=h.unescape(tags[j][1])
                    comb.append((tags[j][0], tags[j][1], tags[j][3], tags[j][-2], tags[j][-1]))

                mergedWord=""
                mergedIdx=comb[0][0]
                mergedPosTag=comb[0][2]
                mergedDepIdx=comb[0][3]
                mergedDepTag=comb[0][4]
                for tag in comb:
                    mergedWord+=tag[1]
                    if not(tag[2]==','):
                        mergedIdx=tag[0]
                        mergedPosTag=tag[2]
                        mergedDepIdx=tag[3]
                        mergedDepTag=tag[4]
                newTags.append((mergedIdx, mergedWord, mergedPosTag, mergedDepIdx, mergedDepTag))
                j+=1
            else:
                newTags.append((tags[j][0],tags[j][1], tags[j][3], tags[j][-2], tags[j][-1]))
                j+=1
#                 print word, word2
        return newTags
    else:
        newTags=[(tag[0], tag[1], tag[3], tag[-2], tag[-1]) for tag in tags]
        return newTags


n=1469
tokens=prod_tweets[n].getTokens()
aligned= __alignDepGraph(tokens, prod_deps[n])
print 'tweet:', prod_tweets[n]
print 'dep t:', prod_deps[n]
print 'align:', aligned
# print prod_twitie[n]
print len(aligned), len(tokens)

# Align the dependancy tokens with the original tokens
prod_depsa=alignDepGraph(prod_tweets, prod_deps)
train_depsa=alignDepGraph(train_tweets, train_deps)
eval_depsa=alignDepGraph(eval_tweets, eval_deps)
test_depsa=alignDepGraph(test_tweets, test_deps)

def fillMissingIdx(depTree):
    keys = sorted(map(int, depTree.keys()))
#     print keys
    for i in range(0, len(keys)-1):
        diff=keys[i+1] - keys[i]
        if  diff> 1:
            for j in range(1, diff):
                key=str(keys[i]+j)
                nxtKey=str(keys[i+1])
#                 print key, nxtKey
                depTree[key]=depTree[nxtKey]

    return depTree

def addDependancyFeatures(docs, deps):
    for tidx, tweet in enumerate(docs):
#         print tidx
        dep=deps[tidx]
        depTree={tagset[0]:tagset for tagset in dep}
        depTree['-1']=('-1', '<NIL>','<NIL>', '-1', '<NIL>')
        depTree['0']=('0', '<ROOT>','<ROOT>', '0', '<ROOT>')
        fillMissingIdx(depTree)

        idepTree=defaultdict(lambda: ('-2', '<NIL>','<NIL>', '-2', '<NIL>'), {tagset[3]:tagset for tagset in dep})
#         for tkn in tweet.getTokens():
        for i,tkn in enumerate(tweet.getTokens()):
            f=tkn.getFeatures()
            depNode=dep[i]
#             print depNode
            f['DEP-1-APOS']=depTree[depNode[3]][2]
            f['DEP-2-APOS_']=depTree[depTree[depNode[3]][3]][2]
            f['DEP-2-APOS']=f['DEP-1-APOS']+","+f['DEP-2-APOS_']

            f['DEP-1-dep']=depTree[depNode[3]][-1]
            f['DEP-2-dep_']=depTree[depTree[depNode[3]][3]][-1]
            f['DEP-2-dep']=f['DEP-1-dep']+","+f['DEP-2-dep_']

            f['DEP-1-word-lower']=depTree[depNode[3]][1].lower()
            f['DEP-2-word-lower']=depTree[depTree[depNode[3]][3]][1].lower()

            f['DEP-INV-1-APOS']=idepTree[depNode[0]][2]
            f['DEP-INV-2-APOS_']=idepTree[idepTree[depNode[0]][0]][2]
            f['DEP-INV-2-APOS']= f['DEP-INV-1-APOS']+","+f['DEP-INV-2-APOS_']

            f['DEP-INV-1-dep']=idepTree[depNode[0]][-1]
            f['DEP-INV-2-dep_']=idepTree[idepTree[depNode[0]][0]][-1]
            f['DEP-INV-2-dep']=f['DEP-INV-1-dep']+","+f['DEP-INV-2-dep_']

            f['DEP-INV-1-word-lower']=idepTree[depNode[0]][1].lower()
            f['DEP-INV-2-word-lower']=idepTree[idepTree[depNode[0]][0]][1].lower()

addDependancyFeatures(prod_tweets, prod_depsa)
addDependancyFeatures(train_tweets, train_depsa)
addDependancyFeatures(eval_tweets, eval_depsa)
addDependancyFeatures(test_tweets, test_depsa)

eval_tweets[1].getTokenFeatureSets()


################################################
### BROWN CLUSTERS #####
################################################

#try brown clusters
file = open('brown_clusters/50mpaths2.txt', 'rb')
clusterCorpus = []
for line in file:
    clusterCorpus.append(line.strip().split('\t'))

def create_brown_dict(corpus):
    train_cluster_dict = defaultdict(lambda:'NA')
    for word in corpus:
        train_cluster_dict[word[1]] = word[0]
    return train_cluster_dict

brown_dict=create_brown_dict(clusterCorpus)

brown_dict['why']

def addBrownFeatures(docs, brown_dict):
    for doc in docs:
        for token in doc.getTokens():
            word=token.text.lower()
            features=token.features
            #only append bc if brown cluster exists
            cid=brown_dict[word]
            features['brown_12']=cid[:12]
            features['brown_8'] = cid[:8]
            features['brown_4'] = cid[:4]

all_tweets=prod_tweets+train_tweets+eval_tweets + test_tweets
addBrownFeatures(all_tweets, brown_dict)
all_tweets[-1]

#Gazetteer features
alan_corpus=corpus.WordListCorpusReader('./dicts/alanritter/', '[a-z]+.*', encoding=None)

typedef=corpus.WordListCorpusReader('./dicts/', 'lists\.def', encoding=None)

class MyDefaultDict(dict):
    def __init__(self, factory):
        self.factory = factory
    def __missing__(self, key):
        self[key] = self.factory(key)
        return self[key]


typeDefDic=MyDefaultDict(lambda k :k.split('.')[0])

################################################
### GAZETTEER FEATURES #####
################################################

# For GATE gazetteer lists
# listTypes=corpus.WordListCorpusReader('./dicts/', 'lists\.def', encoding=None)
# for typedef in listTypes.words():
#     split=typedef.split(':')
#     typeDefDic[split[0]]=split[1]

def create_gaz_dict(corpus, typeDefDic):
    dic=defaultdict(lambda:[])
    files=corpus.fileids()
    for file_id in files:
        entityType=typeDefDic[file_id]
        for word in corpus.words(file_id):
            word=word.lower()
            split=word.split(' ')
            key=split[0]
            lookup=(split,entityType)
            if dic.has_key(key):
                vals=dic[key]
                vals.append(lookup)
            else:
                dic[key]=[lookup]
    return dic

alan_dic=create_gaz_dict(alan_corpus, typeDefDic)
# print alan_dic['joe']
# alan_corpus.words('cap.1000')


def lookup(matches, tokens, i):
    MIN_WINDOW=2
    MAX_WINDOW=len(tokens)-i
    completeMatches=[]
    bestMatch=None

    for window  in range (1,MAX_WINDOW):
        nxtWord=tokens[i+window].text
        nxtMatches=[]
        maxLen=0
#         print window
        for _match in matches:
            match = _match[0]
            matchType=_match[1]
            maxLen=max(len(match), maxLen)
            if len(match)>window:
                if match[window]==nxtWord:
#                     print '----',window, match, matchType
                    nxtMatches.append(_match)
            else:
                completeMatches.append(_match)
        matches=nxtMatches
#     print completeMatch, bestMatch, tokens[i].text
        if(window>maxLen):
            break
    return completeMatches

def addAlanDicFeatures(docs, dic):
    for doc in docs:
        tokens=doc.getTokens()
        for i, token in enumerate(tokens) :
            word=token.text.lower()
            if len(dic[word]) > 0:
                matches = lookup(dic[word], tokens, i)
                if len(matches)>0:
                    addGazFeaturesTo(tokens, i, matches)

def addGazFeaturesTo(tokens, i, matches):
    for match in matches:
        tag='B'
#         print match, len(match[0])
        for j,mtkn in enumerate(match[0]):
#             print len(match[0])
            tokens[i+j].getFeatures()['Gaz-'+match[1]]=tag
            tag='I'

addAlanDicFeatures(all_tweets, alan_dic)
all_tweets[5].getTokenFeatureSets()


################################################
### ORTHOGRAPHIC FEATURES #####
################################################

def isGoodCap(tweet):

    tokens=tweet.getTokens()
    total=len(tokens)
    numAllCaps=0
    numInitCaps=0

    for tkn in tokens:
        word=tkn.getText()
        #remove usernames and hashtags from total, remove single character tokens from total
        if word.startswith('@') or word.startswith('#') or len(word) == 1 :
            total-=1
        else:
            if re.search(r'^[A-Z][a-z]+', word):
                numInitCaps+=1
            elif re.match(r'^[A-Z]+$', word):
                numAllCaps+=1

#     print numInitCaps, numAllCaps
    goodInitCap =  numInitCaps < total
    goodAllCap =  numAllCaps < total
    return goodInitCap , goodAllCap


##Test the method
doc=Document([['YES','O'], ['G','O'],  ['ALL', 'O'], ['CAP', 'O'], ['.', 'O'], ['!', 'O']])
# doc.getTokens()
isGoodCap(doc)

def addOrthographicFeatures(docs):
    for doc in docs:
        goodInitCap , goodAllCap = isGoodCap(doc)
        for t in doc.getTokens():
            word=t.getText()
            f=t.getFeatures()
            f["word"]=  word
            f["word-lower"] = word.lower()
            if(len(word) >= 4):
                f["prefix1"] = word[0:1].lower()
                f["prefix2"]= word[0:2].lower()
                f["prefix3"]= word[0:3].lower()
                f["suffix1"]= word[len(word)-1:len(word)].lower()
                f["suffix2"]= word[len(word)-2:len(word)].lower()
                f["suffix3"]= word[len(word)-3:len(word)].lower()

            if re.search(r'^[A-Z]', word):
                f['INITCAP']= True
            if re.search(r'^[A-Z]', word) and goodInitCap:
                f['INITCAP_AND_GOODCAP']= True
            if re.match(r'^[A-Z]+$', word):
                f['ALLCAP'] = True
            if re.match(r'^[A-Z]+$', word) and goodAllCap:
                f['ALLCAP_AND_GOODCAP'] = True
            if re.match(r'.*[0-9].*', word):
                f['HASDIGIT']= True
            if re.match(r'[0-9]', word):
                f['SINGLEDIGIT']= True
            if re.match(r'[0-9][0-9]', word):
                f['DOUBLEDIGIT']=True
            if re.match(r'.*-.*', word):
                f['HASDASH']=True
            if re.match(r'[.,;:?!-+\'"]', word):
                f['PUNCTUATION']=True

addOrthographicFeatures(all_tweets)
# all_tweets[0]


DOUBLE_QUOTE='"'
SINGLE_QUOTE="'"
QUOTE_SPAN=4
def addQuoteFeature(doc):
    tokens=doc.getTokens();
    i=0
    end=len(tokens)
    while i < end :
        tkn=tokens[i]
        word = tkn.getText()
        quoted=False
        #check double quoted span of 4
        if(word== DOUBLE_QUOTE):
            j=2
            while j< QUOTE_SPAN+2 and i+j<end:
                word2=tokens[i+j].getText()
                if(word2== DOUBLE_QUOTE):
                    quoted=True
                    break
                else:
                    j+=1
            if quoted:
                for k in range(1,j):
                    tokens[i+k].addFeature('QUOTED', True)
                i+=j
        elif(word == SINGLE_QUOTE):
            j=2
            while j< QUOTE_SPAN+2 and i+j<end:
                word2=tokens[i+j].getText()
                if(word2 == SINGLE_QUOTE):
                    quoted=True
                    break
                else:
                    j+=1
            if quoted:
                for k in range(1,j):
                    tokens[i+k].addFeature('QUOTED', True)
                i+=j
        i+=1
    return quoted

doc=Document([['"','O'], ['OUT','O'],  ['OUT', 'O'], ["'", 'O'], ['INSIDE', 'O'], ['INSIDE', 'O'], ['INSIDE', 'O'], ['INSIDE', 'O'], ["'", 'O'], ['OUT', 'O'], ['"', 'O']])
addQuoteFeature(doc)
print doc.getTokenFeatureSets()

for doc in all_tweets:
    addQuoteFeature(doc)

# def getEntities(all_tweets):
#     entities=[]
#     for tweet in all_tweets:
#         labels=tweet.getTokenLabelsAt(0)
#         tokens=tweet.getTokens()
#         ent=""
#         for i,l in enumerate(labels):
#             if(l=="B"):
#                 ent=ent+tokens[i].text
#             elif(l=="I"):
#                 ent=ent+" "+tokens[i].text
#             elif(ent!=""):
#                 entities.append(ent)
#                 ent=""
#     return entities

# entitites=getEntities(all_tweets)
# entitites



################################################
### CONTEXTUAL FEATURES #####
################################################
for tweet in all_tweets:
    #extract features for word tokens
    START='<S>'
    END='</S>'
    f_b2={'APOS': START, 'TPOS':START, 'NPOS':START, 'brown_12':START, 'brown_8': START, 'brown_4':START, 'word-lower':START}
    f_b1=f_b2
    f_n1={'APOS': END, 'TPOS':END, 'NPOS':END, 'brown_12':END, 'brown_8': END, 'brown_4':END, 'word-lower':END}
    f_n2=f_n1
    feats=[f for f in tweet.getTokenFeatureSets()]
    length=len(feats)
    feats.extend([f_n1, f_n2])
    for i in range(0,length):
#         print i, ' ',length, len(feats), feats[i]
        features=feats[i]
        f_n1=feats[i+1]
        f_n2=feats[i+2]
        features['CTX-TPOS-Bfr']= f_b1['TPOS']#+','+f_b2['TPOS']
        features['CTX-TPOS-Nxt']= f_n1['TPOS']#+','+f_n2['TPOS']

        features['CTX-TPOS-Bfr2']= f_b1['TPOS']+','+f_b2['TPOS']
        features['CTX-TPOS-Nxt2']= f_n1['TPOS']+','+f_n2['TPOS']
        features['CTX-TPOS-Bfr2_']=f_b2['TPOS']
        features['CTX-TPOS-Nxt2_']=f_n2['TPOS']

        features['CTX-APOS-Bfr']= f_b1['APOS']#+','+f_b2['APOS']
        features['CTX-APOS-Nxt']= f_n1['APOS']#+','+f_n2['APOS']

        features['CTX-APOS-Bfr2']= f_b1['APOS']+','+f_b2['APOS']
        features['CTX-APOS-Nxt2']= f_n1['APOS']+','+f_n2['APOS']
        features['CTX-APOS-Bfr2_']= f_b2['APOS']
        features['CTX-APOS-Nxt2_']= f_n2['APOS']

        features['CTX-NPOS-Bfr']= f_b1['NPOS']#+','+f_b2['APOS']
        features['CTX-NPOS-Nxt']= f_n1['NPOS']#+','+f_n2['APOS']
        features['CTX-NPOS-Bfr2']= f_b1['NPOS']+','+f_b2['NPOS']
        features['CTX-NPOS-Nxt2']= f_n1['NPOS']+','+f_n2['NPOS']

        features['CTX-b12-Bfr']= f_b1['brown_12']#+','+f_b2['brown_12']
        features['CTX-b12-Nxt']= f_n1['brown_12']#+','+f_n2['brown_12']
        features['CTX-b8-Bfr']= f_b1['brown_8']#+','+f_b2['brown_8']
        features['CTX-b8-Nxt']= f_n1['brown_8']#+','+f_n2['brown_8']
        features['CTX-b4-Bfr']= f_b1['brown_4']#+','+f_b2['brown_4']
        features['CTX-b4-Nxt']= f_n1['brown_4']#+','+f_n2['brown_4']

        features['CTX-b12-Bfr2']= f_b1['brown_12']+','+f_b2['brown_12']
        features['CTX-b12-Nxt2']= f_n1['brown_12']+','+f_n2['brown_12']
        features['CTX-b8-Bfr2']= f_b1['brown_8']+','+f_b2['brown_8']
        features['CTX-b8-Nxt2']= f_n1['brown_8']+','+f_n2['brown_8']
        features['CTX-b4-Bfr2']= f_b1['brown_4']+','+f_b2['brown_4']
        features['CTX-b4-Nxt2']= f_n1['brown_4']+','+f_n2['brown_4']

        features['CTX-b12-Bfr2_']= f_b2['brown_12']
        features['CTX-b12-Nxt2_']= f_n2['brown_12']
        features['CTX-b8-Bfr2_']= f_b2['brown_8']
        features['CTX-b8-Nxt2_']= f_n2['brown_8']
        features['CTX-b4-Bfr2_']= f_b2['brown_4']
        features['CTX-b4-Nxt2_']= f_n2['brown_4']

        features['CTX-word-lower-Bfr']= f_b1['word-lower']#+','+f_b2['APOS']
        features['CTX-word-lower-Nxt']= f_n1['word-lower']#+','+f_n2['APOS']

        f_b2=f_b1
        f_b1=feats[i]

all_tweets[0].getTokenFeatures(5)

################################################
### TRAIN AND EVAL #####
################################################

def bio_classification_report(y_true, y_pred):
    """
    Classification report for a list of BIO-encoded sequences.
    It computes token-level metrics and discards "O" labels.

    Note that it requires scikit-learn 0.15+ (or a version from github master)
    to calculate averages properly!
    """
    lb = LabelBinarizer()
    y_true_combined = lb.fit_transform(list(chain.from_iterable(y_true)))
    y_pred_combined = lb.transform(list(chain.from_iterable(y_pred)))

    tagset = set(lb.classes_) - {'O'}
    tagset = sorted(tagset, key=lambda tag: tag.split('-', 1)[::-1])
    class_indices = {cls: idx for idx, cls in enumerate(lb.classes_)}
    print tagset
    return classification_report(
        y_true_combined,
        y_pred_combined,
        labels = [class_indices[cls] for cls in tagset],
        target_names = tagset,
    )
################################################
### FEATURE ENGINEERING - ABLATION #####
################################################
filter=[
         'APOS',
          'CTX-APOS-Bfr', 'CTX-APOS-Nxt',
#          'CTX-APOS-Bfr2', 'CTX-APOS-Nxt2',
         'CTX-APOS-Bfr2_', 'CTX-APOS-Nxt2_',
         'TPOS',
          'CTX-TPOS-Bfr', 'CTX-TPOS-Nxt',
#          'CTX-TPOS-Bfr2', 'CTX-TPOS-Nxt2',
#           'CTX-TPOS-Bfr2_', 'CTX-TPOS-Nxt2_',
#          'NPOS', 'CTX-NPOS-Nxt', 'CTX-NPOS-Bfr', #Overfits
#          'CTX-NPOS-Nxt2', 'CTX-NPOS-Bfr2',
        'brown_12', 'CTX-b12-Bfr', 'CTX-b12-Nxt',
        'brown_4','CTX-b4-Bfr', 'CTX-b4-Nxt',
        'brown_8', 'CTX-b8-Bfr', 'CTX-b8-Nxt',
        'CTX-b12-Bfr2', 'CTX-b12-Nxt2',
        'CTX-b4-Bfr2', 'CTX-b4-Nxt2',
        'CTX-b8-Bfr2', 'CTX-b8-Nxt2',
        'CTX-b12-Bfr2_', 'CTX-b12-Nxt2_',
        'CTX-b4-Bfr2_', 'CTX-b4-Nxt2_',
        'CTX-b8-Bfr2_', 'CTX-b8-Nxt2_',
#         'word-lower',
        'CTX-word-lower-Nxt' , 'CTX-word-lower-Bfr',
#         'prefix1', 'prefix2', 'prefix3',
#         'suffix1', 'suffix2', 'suffix3',
#         'INITCAP',
        'INITCAP_AND_GOODCAP',
#         'ALLCAP' ,
        'ALLCAP_AND_GOODCAP',
        'HASDIGIT', 'SINGLEDIGIT', 'DOUBLEDIGIT', 'HASDASH',
#         'PUNCTUATION',
        'QUOTED',
        'DEP-1-APOS',
        'DEP-2-APOS_',
#         'DEP-2-APOS',
        'DEP-1-dep',
        'DEP-2-dep_',
#         'DEP-2-dep',
#         'DEP-1-word-lower', 'DEP-2-word-lower',
        'DEP-INV-1-APOS',
        'DEP-INV-2-APOS_',
#         'DEP-INV-2-APOS',
        'DEP-INV-1-dep',
        'DEP-INV-2-dep_',
#         'DEP-INV-2-dep',
#         'DEP-INV-1-word-lower',
#         'DEP-INV-2-word-lower'
        ]
regexFilter=[re.compile('Gaz-.*')]


def filterFeatures(tweetFeats):
    filtered=[]
    for f in tweetFeats:
        f_filtered = { key : f[key] for key in filter if f.has_key(key) }
        for key in f.keys():
            for p in regexFilter:
                if p.match(key):
                    f_filtered[key]=f[key]
        filtered.append(f_filtered)
    return filtered

def extractTrainingSet(tweets):
    tweetsFeat=[]
    tweetsFeatLbl=[]
    for doc in tweets:
        fs=filterFeatures(doc.getTokenFeatureSets())
        lbls=doc.getTokenLabelsAt(0)
        tweetsFeat.append(fs)
        sent=zip(fs,lbls)
        tweetsFeatLbl.append(sent)
    return tweetsFeat, tweetsFeatLbl

crf_prod_tweetsFeat, crf_prod_tweetsFeatLbl =extractTrainingSet(prod_tweets)
crf_train_tweetsFeat, crf_train_tweetsFeatLbl =extractTrainingSet(train_tweets)
crf_eval_tweetsFeat, crf_eval_tweetsFeatLbl =extractTrainingSet(eval_tweets)
crf_test_tweetsFeat, crf_test_tweetsFeatLbl =extractTrainingSet(test_tweets)

# crf_prod_tweetsFeatLbl[0]


def feature_func(tknFeats,idx):
    return tknFeats[idx]

################################################
### EVALUATE DEV #####
################################################

params={
    'c1': 0.1,   # coefficient for L1 penalty
    'c2': 1e-3,  # coefficient for L2 penalty
#     'max_iterations': 1000,  # stop earlier

    # include transitions that are possible, but not observed
#     'feature.possible_transitions': True
}
ct = CRFTagger(feature_func ) #,training_opt=params
ct.train(crf_train_tweetsFeatLbl,'model.crf.tagger')


############Predict###################

preds=ct.tag_sents(crf_eval_tweetsFeat)


def extractEvaluationData(actualFeatLbl , preds ):
    y_true=[]
    y_pred=[]
    for i,pred in enumerate(preds):
        y_pred.append([pfl[1] for pfl in pred])
        y_true.append([fl[1] for fl in actualFeatLbl[i]])
    return y_true, y_pred
# for i,t in enumerate(tagged):
#     print tweet.tokens[i], t[1] , tweet.tokens[i].labels[0]

y_true2, y_pred2 = extractEvaluationData(crf_eval_tweetsFeatLbl, preds)

print 'sample pred'
print eval_tweets[1]
print y_true2[1]
print y_pred2[1]

# crf_eval_tweetsFeatLbl[0]

#################Report###########
print 'DEV EVALUATION RESULTS'
print bio_classification_report(y_true2, y_pred2)



#################################################
###  CROSS VALIDATION ON FINAL TRAINING SET #####
#################################################

def crossValidate(X, Xy, n=3):
    all_y_true=[]
    all_y_pred=[]
    for i in range(0,n):
        X_train, X_test, Xy_train, Xy_test = train_test_split(X, Xy, test_size=0.33, random_state=i)

        cvModel = CRFTagger(feature_func)
        cvModel.train(Xy_train,'cv'+str(i)+'.model.crf.tagger') #put num in model filename
        preds=cvModel.tag_sents(X_test)
        y_true, y_pred=extractEvaluationData(Xy_test, preds)
        all_y_true.extend(y_true)
        all_y_pred.extend(y_pred)
        print bio_classification_report(y_true, y_pred)
    print bio_classification_report(all_y_true, all_y_pred)

print 'CROSS VALIDATION RESULTS'
crossValidate(crf_prod_tweetsFeat, crf_prod_tweetsFeatLbl)


#################################################
###  TRAIN PRODUCTION MODEL #####
#################################################

prodModel = CRFTagger(feature_func)
prodModel.train(crf_prod_tweetsFeatLbl,'prod.model.crf.tagger')
preds=prodModel.tag_sents(crf_test_tweetsFeat)

###  SUBMISSION FILE #####
file_name='submission.txt'
def make_submission_file(y_pred, file_name):
    file = open(file_name, "w")
    for tweet in y_pred:
        for word in tweet:
            file.write(word + '\n')
        file.write('\n')
    file.close()
    print "file written to ", file_name

finalPreds=[]
for p in preds:
    sent=[]
    for t in p:
        sent.append(t[1])
    finalPreds.append(sent)


make_submission_file(finalPreds, file_name)