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

