ARTICLE_FOLDER='/srv/perspect/'
REDIS_URL='redis://localhost:6379'
import env_mongo

def init_mongo():
   env_mongo.init()
