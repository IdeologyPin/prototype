ARTICLE_FOLDER='/srv/perspect/'
REDIS_URL='redis://localhost:6379'
import env_mongo
import app.jobQ as jq



jq.init_RQ()

def init_mongo():
   env_mongo.init()



