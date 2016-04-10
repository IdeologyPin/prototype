import requests
import json
import sys
# from util.Cache import cached

_API_KEY = 'V7lmZgPn7NGdEYSp9DGA8l1AsK5zRy8I'
_HOST = 'http://api.relegence.com/'
_HOST_STAGING = 'http://stage.api.relegence.com/'
_CACHE = {}


class Relegence:
    '''
    Religence API client
    documentation for endpoints are at http://www.aolpublishers.com/support/documentation/relegence/services/

    http://www.aolpublishers.com/support/documentation/relegence/services/stories.md
    aol/aol
    '''

    def __init__(self, API_KEY=_API_KEY):
        self.API_KEY = API_KEY
        self.stories = self.__Stories(self)
        self.trending = self.__Trending(self)
        self.taxonomy = self.__Taxonomy(self)
        self._def_params = {'apikey': self.API_KEY}

    '''
    '''

    class __Trending:
        def __init__(self, outer):
            self.topics = []

    '''
    '''

    class __Stories:
        # __req_base = _HOST_STAGING + 'stories/'
        __req_base = _HOST + 'stories/'
        def __init__(self, outer):
            self.outer = outer

        # @cached
        def by_subject(self, subject_id, num_articles=100, params={}):
            '''
                params={"numDocs"=100}
                125192054 
            '''
            params['withDocs'] = num_articles
            p = merge_dicts(self.outer._def_params, params);
            resp = "hello world"
            try:
                resp = to_json(requests.get(self.__req_base + str(subject_id), params=p, timeout=10))
                # resp = requests.get(self.__req_base + '/' + str(subject_id), params=p, timeout=5).json()
            except TypeError:
                return "TypeError"
            except requests.exceptions.ReadTimeout:
                return "Read Timeout Error"
            except:
                e = sys.exc_info()[0]
                return e
            # return to_json(resp)
            return resp

    class __Taxonomy:
        __req_base = _HOST + '/taxobrowser/'

        def __init__(self, outer):
            self.hierarchy = self.__Hierarchy(outer)
            self.mapper = self.__Mapper(outer)

        def by_node_type(self, node_type_id):
            raise NotImplementedError

        class __Mapper:
            def __init__(self, outer):
                self.outer = outer

        class __Hierarchy:
            req_base = _HOST + '/taxobrowser/hierarchy'
            req_subjects = '/subjects'
            req_nodetypes = 'nodetypes'

            def __init__(self, outer):
                self.outer = outer

            # @cached
            def get_subjects(self, params={}):
                p = merge_dicts(self.outer._def_params, params);
                return to_json(requests.get(self.req_base + self.req_subjects, params=p))

            # @cached
            def get_nodetypes(self, params={}):
                p = merge_dicts(self.outer._def_params, params);
                return to_json(requests.get(self.req_base + self.req_nodetypes, params=p))


def merge_dicts(x, y):
    # return x.update(y);
    return dict(x.items() + y.items())


def to_json(resp):
    # json.dumps(resp)
    if (resp.status_code == 200):
        print resp
        return resp.json()
    else:
        resp.raise_for_status()
