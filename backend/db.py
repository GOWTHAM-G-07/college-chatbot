import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="127.0.0.1",   # use 127.0.0.1 instead of localhost
        port=3306,
        user="root",       # change if your user is different
        password="Tamilsecondmom@26",
        database="college_chatbot_db"
    )