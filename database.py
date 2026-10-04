import mysql.connector


def get_connection():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="ssm12sql",
        database="cultural_calendar"
    )

    return connection   