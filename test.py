# 데이터베이스에 접속해서 데이터 처리하는 테스트 코드
import mysql.connector
from mysql_connection import get_connection

try :
    # DATA INSERT
    # 1. Connect DB
    connection = get_connection()

    # 2. SQL Query
    # query = '''
    #         insert into recipe
    #             (name, description, cook_time, direction)
    #         values
    #             ('된장찌개', '맛있는 된장찌개 만드는 방법',
    #             '30', '된장을 물에 풀어 야채를 넣고 끓여준다.');
    #         '''
    name = '순두부'
    description = '맛있는 순두부찌개 만드는 법'
    cook_time = 45 
    direction = '먼저 고기를 볶은후, 물을 넣고, 순두부 넣고 끓인다.'
    query = '''
            insert into recipe
                (name, description, cook_time, direction)
            values
                (%s ,%s ,%s ,%s);
            '''
    record = (name, description, cook_time, direction )

    # 3. Get Cursor
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