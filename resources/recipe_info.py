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