from redis import Redis
from rq import Queue

rq = None

def init_RQ():
    redis_conn = Redis()
    global rq
    rq = Queue(connection=redis_conn)


def get_RQ():
    return rq