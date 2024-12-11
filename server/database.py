# Updated database schema
import mysql.connector

def connect_db():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="1234",
        database="expense_tracker"
    )
    return connection

def create_tables():
    connection = connect_db()
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255),
            amount DECIMAL(10, 2),
            category VARCHAR(255)
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS budget (
            id INT PRIMARY KEY,
            amount DECIMAL(10, 2)
        )
    """)
    connection.commit()
    connection.close()

create_tables()