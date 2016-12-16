from pygate import *
from pygate.ext.google_nlp import SentimentAnalyserPR
from pygate.ext.spacy_io import SpacyDoc
from pygate.ext.textacy import KeyTermAnnotatorPR
from pygate.prs import SPMRulePR
from pygate.ext.relegence_nlp import RelEntityTagger

class DuplicateClearingPR(PR):
    def __init__(self):
        self.examined_titles = set()

    def process(self, doc):
        '''
        :type SpacyDoc
        :param doc:
        :return:
        '''
        title = doc["title"]
        doc.sents
        if title in self.examined_titles:
            raise ValueError("Duplicate Article: title"+title)
        self.examined_titles.add(title)



class CustomFeatureExtractor(PR):

    def __init__(self, kt=False, ent=False, all_sent =True):
        self.kt = kt
        self.ent = ent
        self.all_sent = all_sent

    def process(self,doc):
        '''
        :type doc SpacyDoc
        :param doc:
        :return:
        '''
        for kt in doc['KeyTerm']:
            sents=doc.query_overlappedby_y(kt, 'Sentence')
            s=sents[0] #type: Annotation
            s.add_relation('key_term', kt)
#             s.set_feature('key_terms', s.get_relation('key_term'))
        for entity in doc['Entity']:
            if len(entity.text)<200:
                sents = doc.query_overlappedby_y(entity, 'Sentence')
                s = sents[0]
                s.add_relation('entity', entity)


        for sent in doc['Sentence']: #type: Annotation
            #watever the filtering
            has_kt=bool(sent.get_relation('key_term'))
            has_ent=bool(sent.get_relation('entity'))

            if (self.kt and has_kt) or (self.ent and has_ent) or self.all_sent:
                sent.set_attribute('FSentence', True)
                sent.set_feature('source_id', doc['source_id'])

class CustomEntityFeatureExtractor(PR):

    def __init__(self, ent_id ):
        self.ent_id

    def process(self,doc):
        doc #type: SpacyDoc
        for sent in doc['Sentence']:  # type: Annotation
            ents=doc.query_overlappedby_y(sent, 'Entity')
            ent_ids=[ent['wikidata'] for ent in ents if 'wikidata' in ent]
            if self.ent_id in ent_ids:
                sent.set_attribute('FSentence', True)

# class CustomKTFeatureExtractor(PR):
#     def __init__(self, kt):
#         self.kt
#
#     def process(self, doc):
#         doc  # type: SpacyDoc
#         for sent in doc['Sentence']:  # type: Annotation
#             ents = doc.query_overlappedby_y(sent, 'KeyTerm')
#             ent_ids = [ent['wikidata'] for ent in ents if 'wikidata' in ent]
#             if self.ent_id in ent_ids:
#                 sent.set_attribute('FSentence', True)


class SentimentHighlighter(PR):

    def process(self,doc):
        '''
        :type doc SpacyDoc
        :param doc:
        :return:
        '''
        NEG_THRESHOLD = -0.75
        POS_THRESHOLD = .25

        pos=[]
        neg=[]
        for sent in doc.sents:
            if 'gs_score' in sent.features:
                score=sent.get_feature('gs_score')
                mag_score = sent.get_feature('gs_magnitude')
                if score > POS_THRESHOLD and score < 1.0 and mag_score and mag_score > 0.5:
                    ann=Annotation(sent.text, sent.tStart, sent.tEnd, sent.cStart, sent.cEnd, 'PosSentiment',doc)
                    pos.append(ann)
                elif score < NEG_THRESHOLD and mag_score and mag_score > 0.5:
                    ann = Annotation(sent.text, sent.tStart, sent.tEnd, sent.cStart, sent.cEnd, 'NegSentiment', doc)
                    neg.append(ann)

        doc.set_annotation_set('PosSentiment', pos)
        doc.set_annotation_set('NegSentiment', neg)

class BratEmbeddingToMongoPR(PR):

    def __init__(self, anno_types):
        self.anno_types=anno_types

    def process(self,doc):
        art=doc['mongo']
        id=0
        art.entities=[]
        for anno_type in self.anno_types:
            if anno_type in doc:
                annots=doc[anno_type]
                for a in annots:
                    id+=1
                    art.entities.append(['T'+str(id), anno_type, [[a.cStart, a.cEnd]]])
        art.save()

