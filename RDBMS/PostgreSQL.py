import hashlib
from typing import Text, Dict, List

import psycopg2
from psycopg2 import OperationalError
from RDBMS import *


class PostgreSQL:
    @staticmethod
    def calc_sha1(raw_data: dict):
        result = ""
        for _, v in raw_data.items():
            result += str(v)

        # Create a new SHA-1 hash object
        sha1 = hashlib.sha1()

        # Update the hash object with the bytes-like object (e.g., string or bytes)
        if len(result) > 0:
            sha1.update(result.encode('utf-8'))  # Assuming data is a string, encode it to bytes
            result = sha1.hexdigest()

        # Get the hexadecimal representation of the hash
        return result

    def __init__(self):
        self.connection = None
        self.logger = Logger
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
            self.logger.info(f"Successfully connected to PostgreSQL database - {DATABASE_HOST}:{DATABASE_PORT}")

        except OperationalError as e:
            self.logger.exception(e)

    def close_connection(self):
        if self.connection:
            self.connection.close()

            # Check if the connection is closed
            if self.connection.closed == YES:
                self.logger.info(f"Successfully closed PostgreSQL connection - {DATABASE_HOST}:{DATABASE_PORT}")
            else:
                self.close_connection()

    def is_postgresql_connected(self):
        if self.connection is not None:
            if self.connection.closed == NO:
                return CONNECTED
        return NOT_CONNECTED

    def add_record(self, table_name: Text, record_data: Dict) -> None:

        #  check connection before using sql instance
        if not self.is_postgresql_connected():
            self.logger.warning(f"Error on adding new record to PostgreSQL while connection is closed - {record_data.values()}")
            return

        try:
            # Create a cursor to execute SQL commands
            cursor = self.connection.cursor()

            # Build the INSERT query
            insert_query = f"INSERT INTO {table_name} ({', '.join(record_data.keys())}) VALUES ({', '.join(['%s'] * len(record_data))})"

            # Execute the INSERT query with the provided data
            cursor.execute(insert_query, list(record_data.values()))

            # Commit the changes to the database
            self.connection.commit()
            self.logger.info(f"Successfully added a new record to PostgreSQL database.")

        except psycopg2.OperationalError as e:
            # If there's an error, print the error message
            self.logger.exception(e)

    def modify_record(self, table_name: Text, record_data: Dict, key: Text, column_key: Text):

        #  check connection before using sql instance
        if not self.is_postgresql_connected():
            self.logger.warning(f"Error on modifying a record in PostgreSQL while connection is closed, Table: {table_name} | Key: {key}")
            return

        try:
            # Create a cursor to execute SQL commands
            cursor = self.connection.cursor()

            # Build the UPDATE query
            update_query = f"UPDATE {table_name} SET {', '.join([f'{key} = %s' for key in record_data.keys()])} WHERE {column_key} = %s"

            # Execute the UPDATE query with the provided data
            cursor.execute(update_query, list(record_data.values()) + [key])

            # Commit the changes to the database
            self.connection.commit()
            self.logger.info(f"Successfully modified a record in PostgreSQL database, Table: {table_name} | Key: {key}")

        except psycopg2.OperationalError as e:
            # If there's an error, print the error message
            self.logger.exception(e)

    def delete_record(self, table_name: Text, key: Text, column_key: Text):

        #  check connection before using sql instance
        if not self.is_postgresql_connected():
            self.logger.warning(f"Error on deleting a record in PostgreSQL while connection is closed, Table: {table_name} | Key: {key}")
            return

        try:
            # Create a cursor to execute SQL commands
            cursor = self.connection.cursor()

            # Build the DELETE query
            delete_query = f"DELETE FROM {table_name} WHERE {column_key} = %s"

            # Execute the DELETE query with the provided data
            cursor.execute(delete_query, (key,))

            # Commit the changes to the database
            self.connection.commit()
            self.logger.info(f"Successfully deleted a record in PostgreSQL database, Table: {table_name} | Key: {key}")

        except psycopg2.OperationalError as e:
            # If there's an error, print the error message
            self.logger.exception(e)

    def fetch_columns(self, table_name: Text) -> List:

        #  check connection before using sql instance
        if not self.is_postgresql_connected():
            self.logger.warning(f"Error on fetch_columns from PostgreSQL while connection is closed, Table: {table_name}")
            return []

        try:
            # Create a cursor to execute SQL commands
            cursor = self.connection.cursor()

            # Query to get column names from the specified table
            query = f"SELECT column_name FROM information_schema.columns WHERE table_name = %s"

            # Execute the query with the specified table name
            cursor.execute(query, (table_name,))

            # Fetch all column names from the result set
            return [row[0] for row in cursor.fetchall()]

        except psycopg2.OperationalError as e:
            # If there's an error, print the error message
            self.logger.exception(e)

    def is_value_exists(self, table_name: Text, column_name: Text, value: Text) -> int:

        #  check connection before using sql instance
        if not self.is_postgresql_connected():
            self.logger.warning(f"Error on searching for value in PostgreSQL while connection is closed, Table: {table_name} | Value: {value}")
            return VALUE_NOT_EXIST

        try:
            # Create a cursor to execute SQL commands
            cursor = self.connection.cursor()

            # Query to check if the value exists in the specified table
            query = f"SELECT EXISTS(SELECT 1 FROM {table_name} WHERE {column_name} = %s)"

            # Execute the query with the specified value
            cursor.execute(query, (value,))

            # Fetch the result (True if value exists, False otherwise)
            result = cursor.fetchone()[0]

            if result:
                return VALUE_EXIST
            else:
                return VALUE_NOT_EXIST

        except psycopg2.OperationalError as e:
            # If there's an error, print the error message
            self.logger.exception(e)

    def create_query(self, sql_query: Text) -> List:

        #  check connection before using sql instance
        if not self.is_postgresql_connected():
            self.logger.warning(f"Error on sending query to PostgreSQL while connection is closed, Query: {sql_query}")
            return VALUE_NOT_EXIST

        try:
            # Create a cursor to execute queries
            with self.connection.cursor() as cursor:
                # Execute the query
                cursor.execute(sql_query)

                # Fetch the result if it's a SELECT query
                result = cursor.fetchall() if cursor.description else None

                # Commit the changes (for non-SELECT queries)
                self.connection.commit()

                # return result from sql
                return result

        except Exception as e:
            self.logger.exception(e)