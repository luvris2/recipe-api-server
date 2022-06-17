import mysql.connector

def get_connection() :
    connection = mysql.connector.connect(
        host='yh-db.ccekp8a5rlv0.ap-northeast-2.rds.amazonaws.com',
        database='recipe',
        user='recipe_user1234',
        password='recipe1234' )
    return connection
