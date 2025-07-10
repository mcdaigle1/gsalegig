import pymysql
import os

def lambda_handler(event, context):
    db_host = os.environ['DB_HOST']
    db_user = os.environ['DB_ADMIN_USER']
    db_pass = os.environ['DB_ADMIN_PASS']
    db_name = os.environ['DB_NAME']
    
    new_user = event['username']
    new_pass = event['password']

    connection = pymysql.connect(host=db_host, user=db_user, password=db_pass, db=db_name)
    
    try:
        with connection.cursor() as cursor:
            cursor.execute(f"CREATE USER '{new_user}'@'%' IDENTIFIED BY '{new_pass}';")
            cursor.execute(f"GRANT ALL PRIVILEGES ON {db_name}.* TO '{new_user}'@'%';")
            connection.commit()
        return { 'status': 'success' }
    except Exception as e:
        return { 'status': 'error', 'message': str(e) }
    finally:
        connection.close()