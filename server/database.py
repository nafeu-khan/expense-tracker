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
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(255) UNIQUE,
            password VARCHAR(255)
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(255),
            name VARCHAR(255),
            amount DECIMAL(10, 2),
            category VARCHAR(255),
            FOREIGN KEY (username) REFERENCES users(username)
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS budget (
            username VARCHAR(255) PRIMARY KEY,
            amount DECIMAL(10, 2),
            FOREIGN KEY (username) REFERENCES users(username)
        )
    """)
    connection.commit()
    connection.close()

create_tables()
