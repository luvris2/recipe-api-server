from flask import Flask
from flask_restful import Api
from resources.recipe import RecipeListResource
from resources.recipe_info import RecipeResource
from resources.recipe_publish import RecipePublishResource
from user import UserRegisterResource, UserLoginResource

# API 서버를 구축하기 위한 기본 구조
app = Flask(__name__)

# restfulAPI 생성
api = Api(app)

# 경로와 리소스(api코드) 연결
api.add_resource(RecipeListResource, '/recipes')
api.add_resource(RecipeResource, '/recipes/<int:recipe_id>')
api.add_resource(RecipePublishResource, '/recipes/<int:recipe_id>/publish') # 공개 설정
api.add_resource(UserRegisterResource, '/users/register') # 회원가입
api.add_resource(UserLoginResource, '/users/login')
if __name__ == '__main__' :
    app.run()