from flask import request
from flask_jwt_extended import get_jwt_identity, jwt_required
import mysql.connector
from mysql_connection import get_connection
from flask_restful import Resource

class RecipeResource(Resource) :
    # 클라이언트로부터 /recipes/3 이런식으로 경리를 처리하므로
    # 숫자는 바뀌므로 변수로 처리해준다.
    def get(self, recipe_id) :
        # DB에서 recipe_id에 들어있는 값에 해당되는 데이터를 셀렉트 해온다.
        

        # DB로부터 데이터를 받아서 클라이언트에 보내준다
        try :
            connection = get_connection()

            query = '''
                        select *
                        from recipe
                        where id = %s;
                    '''
            record = (recipe_id, ) # tuple

            # dictionary=True : Call Key : Value
            # Select Data is Dictionary Type
            cursor = connection.cursor(dictionary=True)
            cursor.execute(query, record)

            # Call select query
            result_list = cursor.fetchall()

            # DB Data type 'TimeStamp' is convert Python data type 'datetime'
            # not send data from json, because convert data save as str type
            i = 0
            for record in result_list :
                result_list[i]['created_at'] = record['created_at'].isoformat()
                result_list[i]['updated_at'] = record['updated_at'].isoformat()
                i += 1

            cursor.close()
            connection.close()

        except mysql.connector.Error as e :
            print(e)
            cursor.close()
            connection.close()
            return {"error" : str(e)}, 503 #HTTPStatus.SERVICE_UNAVAILABLE

        # 정상적으로 됐을 때 200, 기본 값이므로 생략 가능
        return{
            "result" : "success",
            "count" : len(result_list),
            "result_list" : result_list
        }, 200

    # 데이터를 업데이트하는 API들은 put 함수를 사용한다.
    @jwt_required()
    def put(self, recipe_id) :
        # body에서 전달 된 데이터를 처리
        data = request.get_json()

        # API 실행 코드
        try :
            # DATA UPDATE
            # 1. Connect DB
            connection = get_connection()

            user_id = get_jwt_identity()

            # recipe_id = user_id 확인
            query = '''select user_id from recipe where id = %s;'''
            record = (recipe_id, )
            cursor = connection.cursor(dictionary = True)
            cursor.execute(query, record)
            result_list = cursor.fetchall()
            recipe = result_list[0]
            if recipe['user_id'] != user_id :
                cursor.close()
                connection.close()
                return { "error" : "님의 레시피를 수정할 수 없습니다."}



            # 2. SQL Query
            query = '''
                    update recipe set
                        name=%s, description=%s, cook_time=%s, direction=%s
                    where id = %s;
                    '''
            record = (data['name'], data['description'], data['cook_time'], data['direction'], recipe_id)
            # 3. Get Cursor
            cursor = connection.cursor()
            # 4. Execute Query with cursor
            cursor.execute(query, record)
            # 5. DATA commit at DB
            connection.commit()
            # 6. Close Resource
            cursor.close()
            connection.close()

        except mysql.connector.Error as e :
            print(e)
            cursor.close()
            connection.close()
            return {"error" : str(e)}, 503 #HTTPStatus.SERVICE_UNAVAILABLE

        # 정상적으로 됐을 때 200, 기본 값이므로 생략 가능
        return {"result" : "success"}, 200

    # 데이터를 삭제하는 API들은 delete 함수를 사용한다.
    def delete(self, recipe_id) :
        # body에서 전달 된 데이터를 처리
        data = request.get_json()

        # API 실행 코드
        try :
            # DATA DELETE
            # 1. Connect DB
            connection = get_connection()

            # 2. SQL Query
            query = '''
                    delete from recipe
                    where id = %s;
                    '''
            record = (recipe_id, )
            # 3. Get Cursor
            cursor = connection.cursor()
            # 4. Execute Query with cursor
            cursor.execute(query, record)
            # 5. DATA commit at DB
            connection.commit()
            # 6. Close Resource
            cursor.close()
            connection.close()

        except mysql.connector.Error as e :
            print(e)
            cursor.close()
            connection.close()
            return {"error" : str(e)}, 503 #HTTPStatus.SERVICE_UNAVAILABLE

        # 정상적으로 됐을 때 200, 기본 값이므로 생략 가능
        return {"result" : "success"}, 200