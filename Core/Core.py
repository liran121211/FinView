from typing import Text, Dict

from RDBMS import SQL_ERROR
from RDBMS.PostgreSQL import PostgreSQL


class Users:
    def __init__(self):
        self.db = PostgreSQL()

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
        self.db = PostgreSQL()

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
        record_data['sha1_identifier'] = PostgreSQL.calc_sha1(record_data)

        if self.is_primary_key_exist(primary_key=record_data['sha1_identifier']):
            return SQL_ERROR

        self.db.add_record(table_name='transactions', record_data=record_data)

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


users_interface = Users()
users_interface.add_user('liran', '123456')

transactions_interface = Transactions()
transactions_interface.add_transaction(
    record_data={
        'date_of_purchase': '01/01/1980',
        'business_name': 'סתם עסק',
        'charge_amount': 19.0,
        'payment_type': 'עסקה ndghkv',
        'total_amount': 199.0,
    },
    username='liran')
