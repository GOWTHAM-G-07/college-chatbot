import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="college_user",
    password="college123",
    database="college_chatbot_db",
    auth_plugin="mysql_native_password"
)

cursor = conn.cursor(dictionary=True)
