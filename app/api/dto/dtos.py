import json
import bson.json_util as bson


class BaseDto(object):
     def to_json(self):
         return json.dumps(self.__dict__)

     def to_dict(self):
         return self.__dict__

class SubjectListDto(BaseDto):

    def __init__(self,subjects):
        self.subjects = subjects
        self.count = len(subjects)

    @classmethod
    def from_mongo(self, subjects_bson):
        subs=[]
        for s in subjects_bson:
            subs.append(s.to_mongo())
        return  SubjectListDto(subs)



class ClusteringListDto(BaseDto):

    def __init__(self, clusterings):
        self.clusterings=clusterings

    @classmethod
    def from_mongo(self, clusterings_bson):
        clusterings = []
        for c in clusterings_bson:
            json=c.to_mongo()
            json['_id']=str(json['_id'])
            clusterings.append(json)
        return ClusteringListDto(clusterings)


class TrendingStoryListDto(BaseDto):

    def __init__(self, stories):
        self.stories=stories
        self.count=len(stories)

    @classmethod
    def from_relegence(self, relegence_stories):
        stories = []
        for s in relegence_stories['results']:
            # stories[s['_id']] = s['alphaDocs'][0]['headline']
            stories.append({"id":s['_id'], "headline":s['alphaDocs'][0]['headline'], "url":s['alphaDocs'][0]['guid']})
        return TrendingStoryListDto(stories).to_dict()


