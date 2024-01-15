from time import sleep
from typing import Text, Dict

import psycopg2
from psycopg2 import OperationalError
from RDBMS import *


class PostgreSQL:

    def __init__(self):
        self.connection = None
        self.__init_connection()

    def __init_connection(self):
        try:
            # Replace these with your PostgreSQL connection details
            self.connection = psycopg2.connect(
                dbname=DATABASE_NAME,
                user=DATABASE_USER,
                password=DATABASE_PASSWORD,
                host=DATABASE_HOST,
                port=DATABASE_PORT
            )

            # If the connection is successful, print a success message
            print("PostgreSQL connection is successful!")

        except OperationalError as e:
            # If there's an error, print the error message
            print(f"Error: {e}")

    def close_connection(self):
        if self.connection:
            self.connection.close()
            print("Connection closing request sent.")

            # Check if the connection is closed
            if self.connection.closed == INACTIVE:
                print("Connection is closed.")
            else:
                print("Connection is not closed.")

    def add_record(self, table_name: Text, new_data: Dict):
        try:
            # Create a cursor to execute SQL commands
            cursor = self.connection.cursor()

            # Build the INSERT query
            insert_query = f"INSERT INTO {table_name} ({', '.join(new_data.keys())}) VALUES ({', '.join(['%s'] * len(new_data))})"

            # Execute the INSERT query with the provided data
            cursor.execute(insert_query, list(new_data.values()))

            # Commit the changes to the database
            self.connection.commit()

            print("New row added successfully!")

        except psycopg2.OperationalError as e:
            # If there's an error, print the error message
            print(f"Error: {e}")
