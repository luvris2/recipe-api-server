from flask import request
from flask_restful import Resource
import mysql.connector
from mysql_connection import get_connection

class RecipePublishResource(Resource) :
    # 레시피를 공개
    def put(self, recipe_id) :
        data = request.get_json()
        connection = get_connection()
        # recipe_id를 가지고 DB의 is_publish 컬럼을 1로 변경
        try :
            query = '''
                    update recipe set
                        is_publish = 1
                    where id = %s;
                    '''
            record = (recipe_id, )
            cursor = connection.cursor()
            cursor.execute(query, record)
            connection.commit()
            cursor.close()
            connection.close()

        except mysql.connector.Error as e :
            print(e)
            cursor.close()
            connection.close()
            return {"error" : str(e)}, 503 #HTTPStatus.SERVICE_UNAVAILABLE

        # 정상적으로 됐을 때 200, 기본 값이므로 생략 가능
        return {"result" : "success"}, 200

    # 레시피를 임시저장
    def delete(self, recipe_id) :
        # DB의 is_publish 컬럼을 0으로 변경
        data = request.get_json()
        connection = get_connection()
        # recipe_id를 가지고 DB의 is_publish 컬럼을 1로 변경
        try :
            query = '''
                    update recipe set
                        is_publish = 0
                    where id = %s;
                    '''
            record = (recipe_id, )
            cursor = connection.cursor()
            cursor.execute(query, record)
            connection.commit()
            cursor.close()
            connection.close()

        except mysql.connector.Error as e :
            print(e)
            cursor.close()
            connection.close()
            return {"error" : str(e)}, 503 #HTTPStatus.SERVICE_UNAVAILABLE

        # 정상적으로 됐을 때 200, 기본 값이므로 생략 가능
        return {"result" : "success"}, 200

