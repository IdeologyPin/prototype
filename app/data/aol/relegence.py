import requests
import json
from util.Cache import cached

_API_KEY = 'V7lmZgPn7NGdEYSp9DGA8l1AsK5zRy8I'
_HOST = 'http://api.relegence.com/'
_HOST_STAGING = 'http://stage.api.relegence.com/'
_CACHE = {}


class Relegence:
    '''
    Religence API client
    documentation for endpoints are at http://www.aolpublishers.com/support/documentation/relegence/services/
    '''

    def __init__(self, API_KEY=_API_KEY):
        self.API_KEY = API_KEY
        self.stories = self.Stories(self)
        self.trending = self.Trending(self)
        self.taxenomy = self.Taxenomy(self)
        self._def_params = {'apikey': self.API_KEY}

    '''
    '''

    class Trending:
        __req_base = _HOST + 'trending/'
        def __init__(self, outer):
            self.outer=outer
            self.topics = []

        @cached
        def by_subject(self, subject_id, params={}):
            '''
                params={'withDocs': True}
            '''
            p = merge_dicts(self.outer._def_params, params);
            return to_json(requests.get(self.__req_base+'/'+subject_id, params=p))

    '''
    '''

    class Stories:
        __req_base = _HOST_STAGING + 'stories/'

        def __init__(self, outer):
            self.outer = outer

        @cached
        def by_subject(self, subject_id, params={}):
            '''
                params={'withDocs': True}
            '''
            p = merge_dicts(self.outer._def_params, params);
            return to_json(requests.get(self.__req_base+subject_id, params=p))

    class Taxenomy:
        __req_base = _HOST + '/taxobrowser/'

        def __init__(self, outer):
            self.hierarchy = self.__Hierarchy(outer)
            self.mapper = self.__Mapper(outer)
            req_subjects = '/hierarchy/subjects'
            req_nodetypes = '/hierarchy/nodetypes'

        @cached
        def get_subjects_hierarchy(self, params={}):
            p = merge_dicts(self.outer._def_params, params);
            return to_json(requests.get(self.req_base + self.req_subjects, params=p))

        @cached
        def get_nodetypes_hierarchy(self, params={}):
            p = merge_dicts(self.outer._def_params, params);
            return to_json(requests.get(self.req_base + self.req_nodetypes, params=p))


def merge_dicts(x, y):
    # return x.update(y);
    return dict(x.items() + y.items())


def to_json(resp):
    if (resp.status_code == 200):
        return resp.json()
    else:
        resp.raise_for_status()
