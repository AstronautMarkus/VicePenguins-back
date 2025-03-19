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
            print("Database connection established successfully.")  # Debug message
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
            results = cursor.fetchall()  # Fetch all results immediately
            self.connection.commit()
            print(f"Query executed successfully: {query}")  # Debug message
            return results
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return None
        finally:
            cursor.close()  # Ensure the cursor is closed after fetching results

    def commit(self):
        if self.connection:
            try:
                self.connection.commit()
                print("Transaction committed successfully.")  # Debug message
            except mysql.connector.Error as err:
                print(f"Error during commit: {err}")
                raise

    def close(self):
        if self.connection:
            self.connection.close()
            self.connection = None