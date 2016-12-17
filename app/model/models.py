from mongoengine import *

def init_connection():
    connect('perspect_db_v2')


class Meta(Document):
    r_subject_synced = LongField()

    @classmethod
    def get_data(cls):
        return cls.objects.first()


class Subject(Document):
    subject_id = IntField(primary_key=True)
    name = StringField()
    children = ListField(ReferenceField('self'))
    meta = {
        'indexes': [
            '$name'  # text index
        ]
    }

    @classmethod
    def search(cls, words):
        cls.objects().search_text(words).order_by('$text_score')


class Entity(Document):
    pass


class Story(Document):
    story_id = LongField(primary_key=True)
    title = StringField();
    mag_score = IntField();
    num_total_docs = IntField();
    num_original_docs = IntField();
    topic_creation_time= DateTimeField();
    last_topic_activity_time = DateTimeField();

    @classmethod
    def find_by_id(cls, story_id):
        return Story.objects(story_id=story_id).first()


class Article(Document):
    article_id = StringField(primary_key=True);
    story = ReferenceField(Story);
    source = StringField();
    source_id= StringField();
    link = StringField();
    title = StringField();
    snippet = StringField();
    file_name = StringField();
    published = DateTimeField();
    author = StringField();
    text = StringField();

    #annotations
    entities=ListField();

    @classmethod
    def find_by_story(cls, story):
        return cls.objects(story=story)

    @classmethod
    def by_id(cls, id):
        return cls.objects(pk=id).first()

class Centroid(EmbeddedDocument):
    id = StringField()
    name = StringField()
    tags = ListField(StringField())
    vector = ListField(FloatField())
    node_ids=ListField(StringField())


class Node(EmbeddedDocument):
    article = ReferenceField('Article')
    span_ids=ListField(IntField())
    span_type=StringField()
    label = StringField()
    vector = ListField(FloatField())
    scores = MapField(FloatField())  # centroid_id -> float
    link = StringField()


class Clustering(Document):
    name = StringField()
    method = StringField()
    collection_id=StringField()
    clusters = ListField(EmbeddedDocumentField(Centroid))
    nodes = ListField(EmbeddedDocumentField(Node))
    status = StringField()

    @classmethod
    def by_collection_id(cls, collection_id):
        '''
        :param collection_id: can be story_id or subject_id, or any article collection you specified.
        :return:
        '''
        return Clustering.objects(collection_id=collection_id)

class ClusteringEmbedded(EmbeddedDocument):
    name = StringField()
    method = StringField()
    collection_id=StringField()
    clusters = ListField(EmbeddedDocumentField(Centroid))
    nodes = ListField(EmbeddedDocumentField(Node))
    status = StringField()

    @classmethod
    def by_collection_id(cls, collection_id):
        '''
        :param collection_id: can be story_id or subject_id, or any article collection you specified.
        :return:
        '''
        return Clustering.objects(collection_id=collection_id)

class ClusteringList(Document):
    name = StringField()
    method = StringField()
    collection_id = StringField()
    clusterings = ListField(EmbeddedDocumentField(ClusteringEmbedded))
    nodes=MapField(EmbeddedDocumentField(Node))

    @classmethod
    def by_collection_id_and_method(cls, collection_id, method):
        return ClusteringList.objects(collection_id=collection_id, method=method).first()



# {
#     name= "trump stuff";
#     #no entities
#     clusterings =[Clustering{name="Donald Trump", clusters=[Centroid{name='pos', node_ids=['a1', 'a2']}, Centroid{name='neu'}, Centroid{name='neg'}]}, Clustering{name="Smith" ...}]
#     nodes={
#         'a1': Node{ article='a1', link='url....'},
#         'a2': Node{}
#     }
# }
# # private title = "More minorities buying guns following Donald Trumps election";
#     private storyID = 801545936543309824;
#     private entities = ["Donald Trump", "gun control measures", "Smith & Wesson", "minorities"];
#     private clusterings = {
#         "Donald Trump": {"positive": [], "negative": [0,1,2]},
#         "gun control measures": {"positive": [0,2], "negative": [1]},
#         "Smith & Wesson": {"positive": [1,2], "negative": [0]},
#         "minorities": {"positive": [0], "negative": [1,2]}
#     };
#
#     private articles = {
#         0:{"id":"eL2Ks4|1479997942658201000", "title":"Trump's Presidency Is Likely To Have A Big Effect On US Gun Sales", "source":"Newsy Partner Feed", url:"http://www.newsy.com/videos/gun-stores-report-decrease-in-sales-after-trump-s-election/", "publish_date": "2016-11-24"},
#         1:{"id":"A1fVb6|148002575367670500", "title":"Gun sales among black community surges after Trumps victory due to fears of racism", "source":"TheBlaze.com", url:"http://www.theblaze.com/news/2016/11/24/gun-sales-among-black-community-surges-after-trumps-victory-due-to-fears-of-racism/", "publish_date": "2016-11-24"},
#         2:{"id":"oaVWlG|1479963106856234000", "title":"Gun Store Owners Seeing Slow Down In Sales Since Trump Victory", "source":"CBS Pittsburgh", url:"http://pittsburgh.cbslocal.com/2016/11/23/gun-store-owners-seeing-slow-down-in-sales-since-trump-victory/", "publish_date": "2016-11-23"}
#     }