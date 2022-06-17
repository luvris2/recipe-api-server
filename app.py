from flask import Flask
from flask_restful import Api
from resources.recipe import RecipeListResource
from resources.recipe_info import RecipeResource

app = Flask(__name__)

api = Api(app)

# 경로와 리소스(api코드) 연결
api.add_resource(RecipeListResource, '/recipes')
api.add_resource(RecipeResource, '/recipes/<int:recipe_id>')

if __name__ == '__main__' :
    app.run()