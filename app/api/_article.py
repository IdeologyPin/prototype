from flask_restful import Resource
from flask_restful import reqparse
from  app.model import Article

#articles/<int:article-id>
class ArticleAPI(Resource):

    def get(self, article_id):
        a=Article.by_id(article_id)
        return a.to_mongo()