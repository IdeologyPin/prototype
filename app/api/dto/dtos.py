import json
import bson.json_util as bson


class BaseDto(object):
     def to_json(self):
         return json.dumps(self.__dict__)

class SubjectList(BaseDto):

    def __init__(self,subjects):
        self.subjects = subjects
        self.count = len(subjects)

    @classmethod
    def from_mongo(self, subjects_bson):
        subs=[]
        for s in subjects_bson:
            subs.append(s.to_mongo())
        return  SubjectList(subs)



