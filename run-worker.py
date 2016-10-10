import os
import urlparse
from redis import Redis
from rq import Worker, Queue, Connection
import app.tasks.worker_env as env
from app.tasks import *

env.init_spacy()

listen = ['high', 'default']
redis_url = env.REDIS_URL
if not redis_url:
    raise RuntimeError('Set up Redis To Go first.')

urlparse.uses_netloc.append('redis')
url = urlparse.urlparse(redis_url)
conn = Redis(host=url.hostname, port=url.port, db=0, password=url.password)

if __name__ == '__main__':
    with Connection(conn):
        worker = Worker(map(Queue, listen))
        worker.work()
