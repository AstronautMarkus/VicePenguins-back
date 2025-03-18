import os
from dotenv import load_dotenv
import mysql.connector

# Load environment variables from .env file
load_dotenv()

class MySQLConnection:
    def __init__(self):
        self.connection = None

    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host=os.getenv("DB_HOST"),
                user=os.getenv("DB_USER"),
                password=os.getenv("DB_PASSWORD"),
                database=os.getenv("DB_NAME")
            )
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            self.connection = None

    def execute_query(self, query, params=None):
        if not self.connection:
            self.connect()
        if not self.connection:
            raise Exception("Failed to connect to the database.")

        cursor = self.connection.cursor(dictionary=True)
        try:
            cursor.execute(query, params)
            self.connection.commit()
            return cursor.fetchall()
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return None
        finally:
            cursor.close()

    def close(self):
        if self.connection:
            self.connection.close()
            self.connection = None