__author__ = 'sasinda'

import redis

_cache=redis.StrictRedis(host='localhost', port=6379, db=0)

def cached(func):
     def wrapper(*args, **kwargs):
         key=func.__name__ + str(args[1:len(args)])+ str(kwargs)
         if kwargs.get('cache', False) and key in _cache:
             return _cache[key]
         else:
            ret=func(*args, **kwargs);
            _cache.set(key,ret)
            return ret
     return wrapper


# def get_key(func, *args, **kwargs):
#     return