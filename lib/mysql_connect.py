import mysql.connector
import os


def connect():
    return mysql.connector.connect(
        host="127.0.0.1",
        user=os.environ['MYSQL_USER'],
        passwd=os.environ['MYSQL_PASSWORD'],
        database="Incels_jan_2019",
        charset="utf8mb4",
        use_unicode=True,
    )
