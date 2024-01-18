import os
from typing import Text, Dict
from psycopg2.errors import InvalidDatetimeFormat
from DataParser.StatementParser import CalOnlineParser, MaxParser, LeumiParser
from FinCore import PostgreSQL_DB, PROJECT_ROOT
from RDBMS import SQL_ERROR


class Users:
    def __init__(self):
        self.db = PostgreSQL_DB

    def add_user(self, username: Text, password: Text):
        if self.is_primary_key_exist(primary_key=username):
            return SQL_ERROR

        self.db.add_record(table_name='users',
                           record_data=
                           {
                               'username': username,
                               'password': password
                           })

    def modify_user(self, username: Text, password: Text):
        self.db.modify_record(table_name='users',
                              record_data=
                              {
                                  'username': username,
                                  'password': password
                              },
                              column_key='username',
                              key=username
                              )

    def delete_user(self, username: Text):
        self.db.delete_record(table_name='users',
                              column_key='username',
                              key=username
                              )

    def is_primary_key_exist(self, primary_key: Text):
        return self.db.is_value_exists(table_name='users', column_name='username', value=primary_key)


class Transactions:
    def __init__(self):
        self.db = PostgreSQL_DB

    def add_transaction(self, record_data: Dict, username: Text):
        required_columns = self.db.fetch_columns('transactions')

        # validate username existence upon adding.
        if not self.db.is_value_exists(table_name='users', column_name='username', value=username):
            return SQL_ERROR

        # add username as foreign key ( Many->One).
        required_columns.append('username')
        record_data['username'] = username

        # validate transaction columns
        for k, _ in record_data.items():
            if k not in required_columns:
                return SQL_ERROR

        # calculate sha1 value for new added record.
        record_data['sha1_identifier'] = PostgreSQL_DB.calc_sha1(record_data)

        if self.is_primary_key_exist(primary_key=record_data['sha1_identifier']):
            return SQL_ERROR
        try:
            self.db.add_record(table_name='transactions', record_data=record_data)
        except InvalidDatetimeFormat as e:
            print(e)
            return SQL_ERROR

    def modify_transaction(self, record_data: Dict, transaction_id: Text):
        required_columns = self.db.fetch_columns('transactions')

        # validate transaction columns
        for k, _ in record_data.items():
            if k not in required_columns:
                return SQL_ERROR

        self.db.modify_record(table_name='transactions',
                              record_data=record_data,
                              column_key='sha1_identifier',
                              key=transaction_id
                              )

    def delete_transaction(self, transaction_id: Text):
        required_columns = self.db.fetch_columns('transactions')

        # validate transaction columns
        if 'sha1_identifier' not in required_columns:
            return SQL_ERROR

        self.db.delete_record(table_name='transactions',
                              column_key='sha1_identifier',
                              key=transaction_id
                              )

    def is_primary_key_exist(self, primary_key: Text):
        return self.db.is_value_exists(table_name='transactions', column_name='sha1_identifier', value=primary_key)


class Application:
    def __init__(self):
        self.__manage_users = Users()
        self.__manage_transactions = Transactions()

    def load_statements_to_db(self, current_user: Text):
        for root, dirs, files in os.walk(os.path.join(PROJECT_ROOT, os.path.join('Files', 'Input'))):
            for filename in files:
                if root.split(os.path.sep)[-1] == 'Cal':
                    cal_data = CalOnlineParser(file_path=os.path.join(root, filename)).extract_base_data()

                    # add records from statements to database
                    for idx, row in cal_data.iterrows():
                        current_record = {
                            'date_of_purchase': row['date_of_purchase'],
                            'business_name': row['business_name'],
                            'charge_amount': row['charge_amount'],
                            'total_amount': row['total_amount'],
                            'payment_type': row['payment_type'],
                        }
                        self.__manage_transactions.add_transaction(record_data=current_record, username=current_user)

                if root.split(os.path.sep)[-1] == 'Max':
                    max_data = MaxParser(file_path=os.path.join(root, filename)).extract_base_data()

                    # add records from statements to database
                    for idx, row in max_data.iterrows():
                        current_record = {
                            'date_of_purchase': row['date_of_purchase'],
                            'business_name': row['business_name'],
                            'charge_amount': row['charge_amount'],
                            'total_amount': row['total_amount'],
                            'payment_type': row['payment_type'],
                        }
                        self.__manage_transactions.add_transaction(record_data=current_record, username=current_user)

                if root.split(os.path.sep)[-1] == 'Leumi':
                    leumi_data = LeumiParser(file_path=os.path.join(root, filename)).extract_base_data()

                    # add records from statements to database
                    for idx, row in leumi_data.iterrows():
                        current_record = {
                            'date_of_purchase': row['date_of_purchase'],
                            'business_name': row['business_name'],
                            'charge_amount': row['charge_amount'],
                            'total_amount': row['total_amount'],
                            'payment_type': row['payment_type'],
                        }
                        self.__manage_transactions.add_transaction(record_data=current_record, username=current_user)




app = Application()
app.load_statements_to_db(current_user='liran')

exit(0)
users_interface = Users()
users_interface.add_user('liran', '123456')

transactions_interface = Transactions()
transactions_interface.add_transaction(
    record_data={
        'date_of_purchase': '01/01/1981',
        'business_name': 'סתם עסק',
        'charge_amount': 19.0,
        'payment_type': 'עסקה ndghkv',
        'total_amount': 199.0,
    },
    username='liran')
