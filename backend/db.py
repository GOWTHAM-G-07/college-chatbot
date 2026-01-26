import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="college_user",
    password="college@123",
    database="college_chatbot_db"
)

cursor = conn.cursor(dictionary=True)
