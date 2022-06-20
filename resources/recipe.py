from flask import request
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restful import Resource
import mysql.connector
from mysql_connection import get_connection


# API를 만들기 위한 클래스 작성
# 클래스 : 변수와 함수로 구성된 묶음
# 클래스는 상속이 가능
# API를 만들기 위한 클래스는 flask_restful 라이브러리의 Resource class를 상속해서 생성하여야 함
class RecipeListResource(Resource) :
    # restful api의 methods에 해당하는 함수 작성

    # 헤더 부분에 jwt_required()가 존재하지 않으면 get_jwt_identity가 작동하지 않음
    @jwt_required()

    def post(self) :
        # api 실행 코드를 여기에 작성
        # 클라이언트에서 body 부분에 작성한 json을 받아오는 코드
        data = request.get_json()

        # user_id의 토큰화 된 데이터를 다시 원복
        user_id = get_jwt_identity()
        try :
            # DATA INSERT
            # 1. Connect DB
            connection = get_connection()
            # 2. SQL Query
            query = '''
                    insert into recipe
                        (name, description, cook_time, direction, user_id)
                    values
                        (%s, %s, %s, %s, %s);
                    '''
            record = (data['name'], data['description'], data['cook_time'], data['direction'], user_id)
            cursor = connection.cursor()
            # 4. Execute Query with cursor
            #cursor.execute(query)
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

            
    def get(self):
        # 쿼리 스트링으로 오는 데이터는 아래처럼 처리해준다.
        offset = request.args.get('offset')
        limit = request.args.get('limit')

        # DB로부터 데이터를 받아서 클라이언트에 보내준다
        try :
            connection = get_connection()

            query = '''
                        select *
                        from recipe
                        where is_publish = 1
                        limit {}, {};'''.format(offset, limit)
                        
            # dictionary=True : Call Key : Value
            # Select Data is Dictionary Type
            cursor = connection.cursor(dictionary=True)
            cursor.execute(query)

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