from typing import Text, Dict, List, Any

from django.utils.datetime_safe import date
from django.contrib.auth.hashers import make_password
from psycopg2.errors import InvalidDatetimeFormat
from DataParser.StatementParser import CalOnlineParser, MaxParser, LeumiParser
from FinCore import *


class Users:
    def __init__(self):
        self.logger = Logger
        self.db = PostgreSQL_DB

    def add_user(self, username: Text, password: Text, first_name: Text, last_name: Text, email:Text) -> int:
        if self.is_user_exist(username=username):
            return RECORD_EXIST

        self.db.add_record(table_name='auth_user',
                           record_data=
                           {
                               'username': username,
                               'password': make_password(password),
                               'is_superuser': False,
                               'is_staff': False,
                               'is_active': True,
                               'first_name': first_name,
                               'last_name': last_name,
                               'email': email,
                               'date_joined': date.today()
                           })

    def modify_user(self, username: Text, password: Text):
        # TODO: modify specific/more than 1 value by given user id
        self.db.modify_record(table_name='users',
                              record_data=
                              {
                                  'username': username,
                                  'password': password
                              },
                              column_key='username',
                              key=username
                              )

    def delete_user(self, user_id: int):
        self.db.delete_record(table_name='auth_user',
                              column_key='id',
                              key=user_id
                              )

    def is_primary_key_exist(self, primary_key: int):
        return self.db.is_value_exists(table_name='auth_user', column_name='id', value=primary_key)

    def is_user_exist(self, username: Text):
        return self.db.is_value_exists(table_name='auth_user', column_name='username', value=username)


class Transactions:
    def __init__(self):
        self.logger = Logger
        self.db = PostgreSQL_DB

    @staticmethod
    def num_to_month(month: Text) -> int:
        if month == 'January':
            return 1

        if month == 'February':
            return 2

        if month == 'March':
            return 3

        if month == 'April':
            return 4

        if month == 'May':
            return 5

        if month == 'June':
            return 6

        if month == 'July':
            return 7

        if month == 'August':
            return 8

        if month == 'September':
            return 9

        if month == 'October':
            return 10

        if month == 'November':
            return 11

        if month == 'December':
            return 12

    def add_transaction(self, record_data: Dict, username: Text):
        required_columns = self.db.fetch_columns('transactions')

        # validate username existence upon adding.
        if not self.db.is_value_exists(table_name='users', column_name='username', value=username):
            return RECORD_EXIST

        # add username as foreign key ( Many->One).
        required_columns.append('username')
        record_data['username'] = username

        # validate transaction columns
        for k, _ in record_data.items():
            if k not in required_columns:
                self.logger.critical(f"Column: [{k}], is not part of the required_columns.")
                return SQL_QUERY_FAILED

        # calculate sha1 value for new added record.
        record_data['sha1_identifier'] = PostgreSQL_DB.calc_sha1(record_data)

        if self.is_primary_key_exist(primary_key=record_data['sha1_identifier']):
            return RECORD_EXIST
        try:
            self.db.add_record(table_name='transactions', record_data=record_data)
        except InvalidDatetimeFormat as e:
            self.logger.exception(e)
            return SQL_QUERY_FAILED

    def modify_transaction(self, record_data: Dict, transaction_id: Text):
        required_columns = self.db.fetch_columns('transactions')

        # validate transaction columns
        for k, _ in record_data.items():
            if k not in required_columns:
                self.logger.critical(f"Column: [{k}], is not part of the required_columns.")
                return SQL_QUERY_FAILED

        self.db.modify_record(table_name='transactions',
                              record_data=record_data,
                              column_key='sha1_identifier',
                              key=transaction_id
                              )

    def delete_transaction(self, transaction_id: Text):
        required_columns = self.db.fetch_columns('transactions')

        # validate transaction columns
        if 'sha1_identifier' not in required_columns:
            self.logger.critical(f"Column: [sha1_identifier], is not part of the required_columns")
            return SQL_QUERY_FAILED

        self.db.delete_record(table_name='transactions',
                              column_key='sha1_identifier',
                              key=transaction_id
                              )

    def is_primary_key_exist(self, primary_key: Text):
        return self.db.is_value_exists(table_name='transactions', column_name='sha1_identifier', value=primary_key)

    def transaction_query(self, sql_query: Text) -> List:
        return self.db.create_query(sql_query)


class Application:
    def __init__(self):
        self.__manage_users = Users()
        self.__manage_transactions = Transactions()

    def load_statements_to_db(self, current_user: Text):
        for root, dirs, files in os.walk(os.path.join(PROJECT_ROOT, os.path.join('Files', 'Input'))):
            for filename in files:
                if root.split(os.path.sep)[-1] == 'Cal':
                    cal_data = CalOnlineParser(file_path=os.path.join(root, filename)).parse()

                    # add records from statements to database
                    for idx, row in cal_data.iterrows():
                        current_record = {
                            'date_of_purchase': row['date_of_purchase'],
                            'business_name':    row['business_name'],
                            'charge_amount':    row['charge_amount'],
                            'total_amount':     row['total_amount'],
                            'payment_type':     row['payment_type'],
                            'payment_provider': row['payment_provider'],
                        }
                        self.__manage_transactions.add_transaction(record_data=current_record, username=current_user)

                if root.split(os.path.sep)[-1] == 'Max':
                    max_data = MaxParser(file_path=os.path.join(root, filename)).parse()

                    # add records from statements to database
                    for idx, row in max_data.iterrows():
                        current_record = {
                            'date_of_purchase': row['date_of_purchase'],
                            'business_name':    row['business_name'],
                            'charge_amount':    row['charge_amount'],
                            'total_amount':     row['total_amount'],
                            'payment_type':     row['payment_type'],
                            'payment_provider': row['payment_provider'],
                        }
                        self.__manage_transactions.add_transaction(record_data=current_record, username=current_user)

                if root.split(os.path.sep)[-1] == 'Leumi':
                    leumi_data = LeumiParser(file_path=os.path.join(root, filename)).parse()

                    # add records from statements to database
                    for idx, row in leumi_data.iterrows():
                        current_record = {
                            'date_of_purchase': row['date_of_purchase'],
                            'business_name':    row['business_name'],
                            'charge_amount':    row['charge_amount'],
                            'total_amount':     row['total_amount'],
                            'payment_type':     row['payment_type'],
                            'payment_provider': row['payment_provider'],
                        }
                        self.__manage_transactions.add_transaction(record_data=current_record, username=current_user)

    @property
    def ask(self):
        def format_result(result: Any) -> Any:
            if isinstance(result, (int, float, bool, str)):
                return result

            if isinstance(result, (list, tuple)):
                if len(result) == 0:
                    return result

                if len(result) == 1:
                    return result[SINGLE_LIST][SINGLE_TUPLE]

                if len(result) > 0:
                    return result

        def how_much_spent_in_specific_month(selected_month: Text, username: Text):
            query = f"SELECT SUM(total_amount) AS total_sum " \
                    f"FROM (" \
                    f"SELECT total_amount" \
                    f" FROM transactions" \
                    f" WHERE EXTRACT(MONTH FROM date_of_purchase) = {Transactions.num_to_month(selected_month)}" \
                    f" AND username='{username}')" \
                    f" AS subquery;"

            result = self.__manage_transactions.transaction_query(sql_query=query)
            return format_result(result)

        def how_much_spent_in_specific_year(selected_year: int, username: Text):
            query = f"SELECT SUM(total_amount) AS total_sum " \
                    f"FROM (" \
                    f"SELECT total_amount" \
                    f" FROM transactions" \
                    f" WHERE EXTRACT(YEAR FROM date_of_purchase) = {selected_year}" \
                    f" AND username='{username}')" \
                    f" AS subquery;"

            result = self.__manage_transactions.transaction_query(sql_query=query)
            return format_result(result)

        def how_much_spent_in_specific_business(business_name: Text, username: Text):
            query = f"SELECT SUM(total_amount) AS total_sum " \
                    f"FROM (" \
                    f"SELECT total_amount" \
                    f" FROM transactions" \
                    f" WHERE business_name ILIKE '%{business_name}%'" \
                    f" AND username='{username}')" \
                    f" AS subquery;"

            result = self.__manage_transactions.transaction_query(sql_query=query)
            return format_result(result)

        def which_records_by_payment_type(payment_type: Text, username: Text):
            query = f"SELECT * " \
                    f"FROM transactions" \
                    f" WHERE payment_type = '{payment_type}'" \
                    f" AND username='{username}';"

            result = self.__manage_transactions.transaction_query(sql_query=query)
            return format_result(result)

        def which_records_by_business_name(business_name: Text, username: Text):
            query = f"SELECT * " \
                    f"FROM transactions" \
                    f" WHERE business_name ILIKE '%{business_name}%'" \
                    f" AND username='{username}';"

            result = self.__manage_transactions.transaction_query(sql_query=query)
            return format_result(result)

        def which_records_above_amount(amount: float, username: Text):
            query = f"SELECT * " \
                    f"FROM transactions" \
                    f" WHERE total_amount >= '{amount}'" \
                    f" AND username='{username}';"

            result = self.__manage_transactions.transaction_query(sql_query=query)
            return format_result(result)

        def which_records_of_payment_provider(payment_provider: Text, username: Text):
            query = f"SELECT * " \
                    f"FROM transactions" \
                    f" WHERE transactions.payment_provider ILIKE '%{payment_provider}%'" \
                    f" AND username='{username}';"

            result = self.__manage_transactions.transaction_query(sql_query=query)
            return format_result(result)

        def how_many_records_from_specific_business(business_name: Text, username: Text):
            query = f"SELECT COUNT(subquery) AS total_transactions " \
                    f"FROM (" \
                    f"SELECT total_amount" \
                    f" FROM transactions" \
                    f" WHERE business_name ILIKE '%{business_name}%'" \
                    f" AND username='{username}')" \
                    f" AS subquery;"

            result = self.__manage_transactions.transaction_query(sql_query=query)
            return format_result(result)

        return {
            'how_much_spent_in_specific_month': how_much_spent_in_specific_month,
            'how_much_spent_in_specific_year': how_much_spent_in_specific_year,
            'how_much_spent_in_specific_business': how_much_spent_in_specific_business,
            'which_records_by_payment_type': which_records_by_payment_type,
            'which_records_by_business_name': which_records_by_business_name,
            'which_records_above_amount': which_records_above_amount,
            'which_records_of_payment_provider': which_records_of_payment_provider,
            'how_many_records_from_specific_business': how_many_records_from_specific_business,
        }