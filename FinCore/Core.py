from typing import Text, Dict, List, Any

from django.utils.timezone import datetime
from django.contrib.auth.hashers import make_password
from psycopg2.errors import InvalidDatetimeFormat
from DataParser.StatementParser import CalOnlineParser, MaxParser, LeumiParser, BankLeumiParser, IsracardParser, \
    BankMizrahiTefahotParser
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
                               'date_joined': datetime.today()
                           })

    def modify_user(self, user_id: int, username: Text, password: Text) -> int:
        if not self.is_primary_key_exist(primary_key=user_id):
            return RECORD_NOT_EXIST

        self.db.modify_record(table_name='users',
                              record_data=
                              {
                                  'username': username,
                                  'password': password
                              },
                              column_key='user_id',
                              key=user_id
                              )

    def delete_user(self, user_id: int) -> int:
        if not self.is_primary_key_exist(primary_key=user_id):
            return RECORD_NOT_EXIST

        self.db.delete_record(table_name='auth_user',
                              column_key='id',
                              key=user_id
                              )

    def retrieve_user_record(self, username: Text) -> List:
        first_name_idx, last_name_idx = 5, 6
        return self.db.retrieve_record(table_name='auth_user', column='username', value=username, specific_indexes=[first_name_idx, last_name_idx])

    def is_primary_key_exist(self, primary_key: int) -> int:
        return self.db.is_value_exists(table_name='auth_user', column_name='id', value=primary_key)

    def is_user_exist(self, username: Text) -> int:
        return self.db.is_value_exists(table_name='auth_user', column_name='username', value=username)


class CreditCardsTransactions:
    def __init__(self):
        self.logger = Logger
        self.db = PostgreSQL_DB

    def add_transaction(self, record_data: Dict, username: Text) -> int:
        required_columns = self.db.fetch_columns('user_credit_card_transactions')

        # validate username existence upon adding.
        if not self.db.is_value_exists(table_name='auth_user', column_name='username', value=username):
            return RECORD_NOT_EXIST

        # add username as foreign key ( Many->One).
        required_columns.append('username')
        record_data['username'] = username

        # validate transaction columns
        for k, _ in record_data.items():
            if k not in required_columns:
                self.logger.critical(f"Column: [{k}], is not part of the [user_credit_card_transactions] required_columns.")
                return SQL_QUERY_FAILED

        # calculate sha1 value for new added record.
        record_data['sha1_identifier'] = PostgreSQL_DB.calc_sha1(record_data, excluded_keys=[])

        if self.is_primary_key_exist(primary_key=record_data['sha1_identifier']):
            return RECORD_EXIST

        # Generate category value for new added record.
        record_data['transaction_category'] = Gemini_Model.find_business_category(record_data['business_name'])

        try:
            self.db.add_record(table_name='user_credit_card_transactions', record_data=record_data)
            return RECORD_ADDED
        except InvalidDatetimeFormat as e:
            self.logger.exception(e)
            return SQL_QUERY_FAILED


    def modify_transaction(self, record_data: Dict, transaction_id: Text) -> int:
        required_columns = self.db.fetch_columns('user_credit_card_transactions')

        # validate transaction columns
        for k, _ in record_data.items():
            if k not in required_columns:
                self.logger.critical(f"Column: [{k}], is not part of the [user_credit_card_transactions] required_columns.")
                return SQL_QUERY_FAILED

        # validate username existence upon modifying.
        if not self.db.is_value_exists(table_name='user_credit_card_transactions', column_name='username', value=record_data['username']):
            return RECORD_NOT_EXIST

        if not self.is_primary_key_exist(primary_key=record_data['sha1_identifier']):
            return RECORD_NOT_EXIST

        self.db.modify_record(table_name='user_credit_card_transactions',
                              record_data=record_data,
                              column_key='sha1_identifier',
                              key=transaction_id
                              )

    def delete_transaction(self, sha1_identifier: Text) -> int:
        required_columns = self.db.fetch_columns('user_credit_card_transactions')

        # validate transaction columns
        if 'sha1_identifier' not in required_columns:
            self.logger.critical(f"Column: [sha1_identifier], is not part of the [user_credit_card_transactions] required_columns.")
            return SQL_QUERY_FAILED

        if not self.is_primary_key_exist(primary_key=sha1_identifier):
            return RECORD_NOT_EXIST

        self.db.delete_record(table_name='user_credit_card_transactions',
                              column_key='sha1_identifier',
                              key=sha1_identifier
                              )

    def is_primary_key_exist(self, primary_key: Text) -> int:
        return self.db.is_value_exists(table_name='user_credit_card_transactions', column_name='sha1_identifier', value=primary_key)

    def transaction_query(self, sql_query: Text) -> List:
        return self.db.create_query(sql_query)


class BankTransactions:
    def __init__(self):
        self.logger = Logger
        self.db = PostgreSQL_DB

    def add_transaction(self, record_data: Dict, username: Text) -> int:
        required_columns = self.db.fetch_columns('user_bank_transactions')

        # validate username existence upon adding.
        if not self.db.is_value_exists(table_name='auth_user', column_name='username', value=username):
            return RECORD_NOT_EXIST

        # add username as foreign key ( Many->One).
        required_columns.append('username')
        record_data['username'] = username

        # validate transaction columns
        for k, _ in record_data.items():
            if k not in required_columns:
                self.logger.critical(f"Column: [{k}], is not part of the [user_bank_transactions] required_columns.")
                return SQL_QUERY_FAILED

        # calculate sha1 value for new added record.
        record_data['sha1_identifier'] = PostgreSQL_DB.calc_sha1(record_data, excluded_keys=[])

        if self.is_primary_key_exist(primary_key=record_data['sha1_identifier']):
            return RECORD_EXIST

        # Generate category value for new added record.
        record_data['transaction_category'] = Gemini_Model.find_bank_transaction_category(record_data['transaction_description'])

        try:
            self.db.add_record(table_name='user_bank_transactions', record_data=record_data)
            return RECORD_ADDED
        except InvalidDatetimeFormat as e:
            self.logger.exception(e)
            return SQL_QUERY_FAILED

    def modify_transaction(self, record_data: Dict, sha1_identifier: Text) -> int:
        required_columns = self.db.fetch_columns('user_bank_transactions')

        # validate transaction columns
        for k, _ in record_data.items():
            if k not in required_columns:
                self.logger.critical(f"Column: [{k}], is not part of the [user_bank_transactions] required_columns.")
                return SQL_QUERY_FAILED

        # validate username existence upon modifying.
        if not self.db.is_value_exists(table_name='user_bank_transactions', column_name='username', value=record_data['username']):
            return RECORD_NOT_EXIST

        if not self.is_primary_key_exist(primary_key=record_data['sha1_identifier']):
            return RECORD_NOT_EXIST

        self.db.modify_record(table_name='user_bank_transactions',
                              record_data=record_data,
                              column_key='sha1_identifier',
                              key=sha1_identifier
                              )

    def delete_transaction(self, sha1_identifier: Text) -> int:
        required_columns = self.db.fetch_columns('user_bank_transactions')

        # validate transaction columns
        if 'sha1_identifier' not in required_columns:
            self.logger.critical(f"Column: [sha1_identifier], is not part of the [user_bank_transactions] required_columns.")
            return SQL_QUERY_FAILED

        if not self.is_primary_key_exist(primary_key=sha1_identifier):
            return RECORD_NOT_EXIST

        self.db.delete_record(table_name='user_bank_transactions',
                              column_key='sha1_identifier',
                              key=sha1_identifier
                              )

    def is_primary_key_exist(self, primary_key: Text) -> int:
        return self.db.is_value_exists(table_name='user_bank_transactions', column_name='sha1_identifier', value=primary_key)

    def transaction_query(self, sql_query: Text) -> List:
        return self.db.create_query(sql_query)


class UserFinancialInformation:
    def __init__(self):
        self.logger = Logger
        self.db = PostgreSQL_DB

    def add_information(self, record_data: Dict, username: Text) -> int:
        required_columns = self.db.fetch_columns('user_information')

        # validate username existence upon adding.
        if not self.db.is_value_exists(table_name='auth_user', column_name='username', value=username):
            return RECORD_NOT_EXIST

        # add username as foreign key ( Many->One).
        required_columns.append('username')
        record_data['username'] = username

        # validate transaction columns
        for k, _ in record_data.items():
            if k not in required_columns:
                self.logger.critical(f"Column: [{k}], is not part of the [user_information] required_columns.")
                return SQL_QUERY_FAILED

        if self.is_primary_key_exist(primary_key=record_data['username']):
            return RECORD_EXIST
        try:
            self.db.add_record(table_name='user_information', record_data=record_data)
        except InvalidDatetimeFormat as e:
            self.logger.exception(e)
            return SQL_QUERY_FAILED

    def modify_information(self, record_data: Dict, username: Text) -> int:
        required_columns = self.db.fetch_columns('user_information')

        # validate transaction columns
        for k, _ in record_data.items():
            if k not in required_columns:
                self.logger.critical(f"Column: [{k}], is not part of the [user_information] required_columns.")
                return SQL_QUERY_FAILED

        # validate username existence upon modifying.
        if not self.is_primary_key_exist(primary_key=username):
            return RECORD_NOT_EXIST

        self.db.modify_record(table_name='user_information',
                              record_data=record_data,
                              column_key='username',
                              key=username
                              )

    def delete_information(self, username: Text) -> int:
        required_columns = self.db.fetch_columns('user_information')

        # validate transaction columns
        if 'username' not in required_columns:
            self.logger.critical(f"Column: [username], is not part of the required_columns")
            return SQL_QUERY_FAILED

        if not self.is_primary_key_exist(primary_key=username):
            return RECORD_NOT_EXIST

        self.db.delete_record(table_name='user_information',
                              column_key='username',
                              key=username
                              )

    def is_primary_key_exist(self, primary_key: Any) -> int:
        return self.db.is_value_exists(table_name='auth_user', column_name='username', value=primary_key)


class UserDirectDebitSubscriptions:
    def __init__(self):
        self.logger = Logger
        self.db = PostgreSQL_DB

    def add_direct_debit_or_subscription(self, record_data: Dict, username: Text) -> int:
        required_columns = self.db.fetch_columns('user_direct_debit_subscriptions')

        # validate username existence upon adding.
        if not self.db.is_value_exists(table_name='auth_user', column_name='username', value=username):
            return RECORD_NOT_EXIST

        # add username as foreign key ( Many->One).
        required_columns.append('username')
        record_data['username'] = username

        # validate transaction columns
        for k, _ in record_data.items():
            if k not in required_columns:
                self.logger.critical(f"Column: [{k}], is not part of the [user_direct_debit_subscription] required_columns.")
                return SQL_QUERY_FAILED

        # calculate sha1 value for new added record.
        record_data['sha1_identifier'] = PostgreSQL_DB.calc_sha1(record_data, excluded_keys=[])

        if self.is_primary_key_exist(primary_key=record_data['sha1_identifier']):
            return RECORD_EXIST
        try:
            self.db.add_record(table_name='user_direct_debit_subscriptions', record_data=record_data)
        except InvalidDatetimeFormat as e:
            self.logger.exception(e)
            return SQL_QUERY_FAILED

    def modify_direct_debit_or_subscription(self, record_data: dict) -> int:
        required_columns = self.db.fetch_columns('user_direct_debit_subscriptions')

        # validate transaction columns
        for k, _ in record_data.items():
            if k not in required_columns:
                self.logger.critical(f"Column: [{k}], is not part of the [user_direct_debit_subscriptions] required_columns.")
                return SQL_QUERY_FAILED

        # validate username existence upon modifying.
        if not self.is_primary_key_exist(primary_key=record_data['sha1_identifier']):
            return RECORD_NOT_EXIST

        self.db.modify_record(table_name='user_direct_debit_subscriptions',
                              record_data=record_data,
                              column_key='sha1_identifier',
                              key=record_data['sha1_identifier']
                              )

    def delete_direct_debit_or_subscription(self, sha1_identifier: Text) -> int:
        required_columns = self.db.fetch_columns('user_direct_debit_subscriptions')

        # validate transaction columns
        if 'sha1_identifier' not in required_columns:
            self.logger.critical(f"Column: [sha1_identifier], is not part of the [user_direct_debit_subscriptions] required_columns.")
            return SQL_QUERY_FAILED

        if not self.is_primary_key_exist(primary_key=sha1_identifier):
            return RECORD_NOT_EXIST

        self.db.delete_record(table_name='user_direct_debit_subscriptions',
                              column_key='sha1_identifier',
                              key=sha1_identifier
                              )

    def is_primary_key_exist(self, primary_key: Any) -> int:
        return self.db.is_value_exists(table_name='user_direct_debit_subscriptions', column_name='sha1_identifier', value=primary_key)


class UserCards:
    def __init__(self):
        self.logger = Logger
        self.db = PostgreSQL_DB

    def add_card(self, record_data: Dict, username: Text) -> int:
        required_columns = self.db.fetch_columns('user_cards')

        # validate username existence upon adding.
        if not self.db.is_value_exists(table_name='auth_user', column_name='username', value=username):
            return RECORD_NOT_EXIST

        # add username as foreign key ( Many->One).
        required_columns.append('username')
        record_data['username'] = username

        # validate transaction columns
        for k, _ in record_data.items():
            if k not in required_columns:
                self.logger.critical(f"Column: [{k}], is not part of the [user_cards] required_columns.")
                return SQL_QUERY_FAILED

        # calculate sha1 value for new added record.
        record_data['sha1_identifier'] = PostgreSQL_DB.calc_sha1(record_data, excluded_keys=['card_type'])

        if self.is_primary_key_exist(primary_key=record_data['sha1_identifier']):
            return RECORD_EXIST
        try:
            self.db.add_record(table_name='user_cards', record_data=record_data)
        except InvalidDatetimeFormat as e:
            self.logger.exception(e)
            return SQL_QUERY_FAILED

    def modify_card(self, record_data: dict) -> int:
        required_columns = self.db.fetch_columns('user_cards')

        # validate transaction columns
        for k, _ in record_data.items():
            if k not in required_columns:
                self.logger.critical(f"Column: [{k}], is not part of the [user_cards] required_columns.")
                return SQL_QUERY_FAILED

        # validate username existence upon modifying.
        if not self.is_primary_key_exist(primary_key=record_data['sha1_identifier']):
            return RECORD_NOT_EXIST

        self.db.modify_record(table_name='user_cards',
                              record_data=record_data,
                              column_key='sha1_identifier',
                              key=record_data['sha1_identifier']
                              )

    def delete_card(self, sha1_identifier: Text) -> int:
        required_columns = self.db.fetch_columns('user_cards')

        # validate transaction columns
        if 'sha1_identifier' not in required_columns:
            self.logger.critical(f"Column: [sha1_identifier], is not part of the [user_cards] required_columns.")
            return SQL_QUERY_FAILED

        if not self.is_primary_key_exist(primary_key=sha1_identifier):
            return RECORD_NOT_EXIST

        self.db.delete_record(table_name='user_cards',
                              column_key='sha1_identifier',
                              key=sha1_identifier
                              )

    def is_primary_key_exist(self, primary_key: Any) -> int:
        return self.db.is_value_exists(table_name='user_cards', column_name='sha1_identifier', value=primary_key)


class Application:
    def __init__(self):
        self.__manage_users = Users()
        self.__manage_user_cards = UserCards()
        self.__manage_credit_cards_transactions = CreditCardsTransactions()
        self.__manage_bank_transactions = BankTransactions()
        self.__manage_user_financial_information = UserFinancialInformation()
        self.__manage_user_direct_debit_subscriptions = UserDirectDebitSubscriptions()

    def load_statements_to_db(self, current_user: Text, folder_path: Text) -> List:
        # identify files structure
        statements_list = self.find_statements_providers(folder_path=folder_path)

        if len(statements_list.keys()) == 0:
            return []

        # TOTAL / ADDED / FAILED / EXIST
        total, added, failed, exist = 0, 1, 2, 3
        statements_stats = [0, 0, 0, 0]

        for filename, statement_provider in statements_list.items():
            if statement_provider == 'Cal':
                # create instance & validate statement
                cal_data = CalOnlineParser(file_path=os.path.join(folder_path, filename))
                cal_data.validate_file_structure()

                # add records from statements to database
                for idx, row in cal_data.parse().iterrows():
                    current_credit_card_transaction_record = {
                        'date_of_transaction':      row['date_of_transaction'],
                        'business_name':            row['business_name'],
                        'charge_amount':            row['charge_amount'],
                        'total_amount':             row['total_amount'],
                        'transaction_type':         row['transaction_type'],
                        'transaction_provider':     row['transaction_provider'],
                        'last_4_digits':            row['last_4_digits'],
                    }
                    result = self.__manage_credit_cards_transactions.add_transaction(record_data=current_credit_card_transaction_record, username=current_user)

                    # statements statistics
                    if result == RECORD_ADDED:
                        statements_stats[added] += 1
                    if result == SQL_QUERY_FAILED or result == RECORD_NOT_EXIST:
                        statements_stats[failed] += 1
                    if result == RECORD_EXIST:
                        statements_stats[exist] += 1
                    statements_stats[total] += 1

                    if len(row[(row == 'עסקת תשלומים') | (row == 'הוראת קבע')]) > 0:
                        current_direct_debit_subscription_record = {
                            'amount':               row['charge_amount'],
                            'payment_type':         row[(row == 'עסקת תשלומים') | (row == 'הוראת קבע')]['transaction_type'],
                            'provider_name':        row['business_name'],
                        }
                        self.__manage_user_direct_debit_subscriptions.add_direct_debit_or_subscription(record_data=current_direct_debit_subscription_record, username=current_user)

                    current_card_record = {
                        'last_4_digits':            row['last_4_digits'],
                        'card_type':                row['card_type'],
                        'issuer_name':              row['transaction_provider'],
                        'full_name':                ' '.join(self.__manage_users.retrieve_user_record(current_user)),
                        }
                    self.__manage_user_cards.add_card(record_data=current_card_record, username=current_user)

            if statement_provider == 'Max':
                # create instance & validate statement
                max_data = MaxParser(file_path=os.path.join(folder_path, filename))
                max_data.validate_file_structure()

                # add records from statements to database
                for idx, row in max_data.parse().iterrows():
                    current_record = {
                        'date_of_transaction':  row['date_of_transaction'],
                        'business_name':        row['business_name'],
                        'charge_amount':        row['charge_amount'],
                        'total_amount':         row['total_amount'],
                        'transaction_type':     row['transaction_type'],
                        'transaction_provider': row['transaction_provider'],
                        'last_4_digits':        row['last_4_digits'],
                    }
                    result = self.__manage_credit_cards_transactions.add_transaction(record_data=current_record, username=current_user)

                    # statements statistics
                    if result == RECORD_ADDED:
                        statements_stats[added] += 1
                    if result == SQL_QUERY_FAILED or result == RECORD_NOT_EXIST:
                        statements_stats[failed] += 1
                    if result == RECORD_EXIST:
                        statements_stats[exist] += 1
                    statements_stats[total] += 1

                    if len(row[(row == 'עסקת תשלומים') | (row == 'הוראת קבע')]) > 0:
                        current_direct_debit_subscription_record = {
                            'amount':               row['charge_amount'],
                            'payment_type':         row[(row == 'עסקת תשלומים') | (row == 'הוראת קבע')]['transaction_type'],
                            'provider_name':        row['business_name'],
                        }
                        self.__manage_user_direct_debit_subscriptions.add_direct_debit_or_subscription(record_data=current_direct_debit_subscription_record, username=current_user)

                    current_card_record = {
                        'last_4_digits':            row['last_4_digits'],
                        'card_type':                row['card_type'],
                        'issuer_name':              row['transaction_provider'],
                        'full_name':                ' '.join(self.__manage_users.retrieve_user_record(current_user)),
                        }
                    self.__manage_user_cards.add_card(record_data=current_card_record, username=current_user)

            if statement_provider == 'Leumi':
                # create instance & validate statement
                leumi_data = LeumiParser(file_path=os.path.join(folder_path, filename))
                leumi_data.validate_file_structure()

                # add records from statements to database
                for idx, row in leumi_data.parse().iterrows():
                    current_record = {
                        'date_of_transaction':  row['date_of_transaction'],
                        'business_name':        row['business_name'],
                        'charge_amount':        row['charge_amount'],
                        'total_amount':         row['total_amount'],
                        'transaction_type':     row['transaction_type'],
                        'transaction_provider': row['transaction_provider'],
                        'last_4_digits':        row['last_4_digits'],
                    }
                    result = self.__manage_credit_cards_transactions.add_transaction(record_data=current_record, username=current_user)

                    # statements statistics
                    if result == RECORD_ADDED:
                        statements_stats[added] += 1
                    if result == SQL_QUERY_FAILED or result == RECORD_NOT_EXIST:
                        statements_stats[failed] += 1
                    if result == RECORD_EXIST:
                        statements_stats[exist] += 1
                    statements_stats[total] += 1

                    if len(row[(row == 'עסקת תשלומים') | (row == 'הוראת קבע')]) > 0:
                        current_direct_debit_subscription_record = {
                            'amount':               row['charge_amount'],
                            'payment_type':         row[(row == 'עסקת תשלומים') | (row == 'הוראת קבע')]['transaction_type'],
                            'provider_name':        row['business_name'],
                        }
                        self.__manage_user_direct_debit_subscriptions.add_direct_debit_or_subscription(record_data=current_direct_debit_subscription_record, username=current_user)

                    current_card_record = {
                        'last_4_digits':            row['last_4_digits'],
                        'card_type':                row['card_type'],
                        'issuer_name':              row['transaction_provider'],
                        'full_name':                ' '.join(self.__manage_users.retrieve_user_record(current_user)),
                        }
                    self.__manage_user_cards.add_card(record_data=current_card_record, username=current_user)

            if statement_provider == 'Isracard':
                # create instance & validate statement
                isracard_data = IsracardParser(file_path=os.path.join(folder_path, filename))
                isracard_data.validate_file_structure()

                # add records from statements to database
                for idx, row in isracard_data.parse().iterrows():
                    current_record = {
                        'date_of_transaction':  row['date_of_transaction'],
                        'business_name':        row['business_name'],
                        'charge_amount':        row['charge_amount'],
                        'total_amount':         row['total_amount'],
                        'transaction_type':     row['transaction_type'],
                        'transaction_provider': row['transaction_provider'],
                        'last_4_digits':        row['last_4_digits'],
                    }
                    result = self.__manage_credit_cards_transactions.add_transaction(record_data=current_record, username=current_user)

                    # statements statistics
                    if result == RECORD_ADDED:
                        statements_stats[added] += 1
                    if result == SQL_QUERY_FAILED or result == RECORD_NOT_EXIST:
                        statements_stats[failed] += 1
                    if result == RECORD_EXIST:
                        statements_stats[exist] += 1
                    statements_stats[total] += 1

                    if len(row[(row == 'עסקת תשלומים') | (row == 'הוראת קבע')]) > 0:
                        current_direct_debit_subscription_record = {
                            'amount':           row['charge_amount'],
                            'payment_type':     row[(row == 'עסקת תשלומים') | (row == 'הוראת קבע')]['transaction_type'],
                            'provider_name':    row['business_name'],
                        }
                        self.__manage_user_direct_debit_subscriptions.add_direct_debit_or_subscription(record_data=current_direct_debit_subscription_record, username=current_user)

                    current_card_record = {
                        'last_4_digits':    row['last_4_digits'],
                        'card_type':        row['card_type'],
                        'issuer_name':      row['transaction_provider'],
                        'full_name': ' '.join(self.__manage_users.retrieve_user_record(current_user)),
                    }
                    self.__manage_user_cards.add_card(record_data=current_card_record, username=current_user)

            if statement_provider == 'BankLeumi':
                # create instance & validate statement
                bank_leumi_data = BankLeumiParser(file_path=os.path.join(folder_path, filename))
                bank_leumi_data.validate_file_structure()

                # add records from statements to database
                for idx, row in bank_leumi_data.parse().iterrows():
                    current_record = {
                        'transaction_date':         row['transaction_date'],
                        'transaction_description':  row['transaction_description'],
                        'transaction_reference':    row['transaction_reference'],
                        'income_balance':           row['income_balance'],
                        'outcome_balance':          row['outcome_balance'],
                        'current_balance':          row['current_balance'],
                        'account_number':           row['account_number'],
                        'transaction_provider':     row['transaction_provider'],
                    }
                    result = self.__manage_bank_transactions.add_transaction(record_data=current_record, username=current_user)

                    # statements statistics
                    if result == RECORD_ADDED:
                        statements_stats[added] += 1
                    if result == SQL_QUERY_FAILED or result == RECORD_NOT_EXIST:
                        statements_stats[failed] += 1
                    if result == RECORD_EXIST:
                        statements_stats[exist] += 1
                    statements_stats[total] += 1

                # extract current bank balance (last loaded statement)
                current_debit = BankLeumiParser.extract_current_bank_debit(bank_leumi_data.data)
                self.__manage_user_financial_information.modify_information(username=current_user,record_data={'current_debit': current_debit})

            if statement_provider == 'BankMizrahiTefahot':
                # create instance & validate statement
                bank_mizrahi_tefahot_data = BankMizrahiTefahotParser(file_path=os.path.join(folder_path, filename))
                bank_mizrahi_tefahot_data.validate_file_structure()
                bank_mizrahi_tefahot_data = bank_mizrahi_tefahot_data.parse()

                # add records from statements to database
                for idx, row in bank_mizrahi_tefahot_data.iterrows():
                    current_record = {
                        'transaction_date':         row['transaction_date'],
                        'transaction_description':  row['transaction_description'],
                        'transaction_reference':    row['transaction_reference'],
                        'income_balance':           row['income_balance'],
                        'outcome_balance':          row['outcome_balance'],
                        'current_balance':          row['current_balance'],
                        'account_number':           row['account_number'],
                        'transaction_provider':     row['transaction_provider'],
                    }
                    result = self.__manage_bank_transactions.add_transaction(record_data=current_record, username=current_user)

                    # statements statistics
                    if result == RECORD_ADDED:
                        statements_stats[added] += 1
                    if result == SQL_QUERY_FAILED or result == RECORD_NOT_EXIST:
                        statements_stats[failed] += 1
                    if result == RECORD_EXIST:
                        statements_stats[exist] += 1
                    statements_stats[total] += 1

                # extract current bank balance (last loaded statement)
                current_debit = BankMizrahiTefahotParser.extract_current_bank_debit(bank_mizrahi_tefahot_data)
                self.__manage_user_financial_information.modify_information(username=current_user,record_data={'current_debit': current_debit})

        return statements_stats

    @staticmethod
    def find_statements_providers(folder_path: Text):
        result = {}
        for root, dirs, files in os.walk(folder_path):
            for filename in files:
                if CalOnlineParser(file_path=os.path.join(root, filename)).validate_file_structure():
                    result[filename] = 'Cal'
                if MaxParser(file_path=os.path.join(root, filename)).validate_file_structure():
                    result[filename] = 'Max'
                if LeumiParser(file_path=os.path.join(root, filename)).validate_file_structure():
                    result[filename] = 'Leumi'
                if IsracardParser(file_path=os.path.join(root, filename)).validate_file_structure():
                    result[filename] = 'IsraCard'
                if BankLeumiParser(file_path=os.path.join(root, filename)).validate_file_structure():
                    result[filename] = 'BankLeumi'
                if BankMizrahiTefahotParser(file_path=os.path.join(root, filename)).validate_file_structure():
                    result[filename] = 'BankMizrahiTefahot'
        return result

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

        def how_much_spent_in_specific_date_bank(selected_month: Text, selected_year: int, username: Text):
            query = f"SELECT SUM(outcome_balance) AS total_sum " \
                    f"FROM (" \
                    f"SELECT outcome_balance" \
                    f" FROM user_bank_transactions" \
                    f" WHERE EXTRACT(MONTH FROM transaction_date) = {num_to_month(selected_month)}" \
                    f" AND EXTRACT(YEAR FROM transaction_date) =  {selected_year}" \
                    f" AND username='{username}')" \
                    f" AS subquery;"

            result = self.__manage_bank_transactions.transaction_query(sql_query=query)
            return format_result(result)

        def how_much_spent_in_specific_date_card(selected_month: Text, selected_year: int, username: Text):
            query = f"SELECT SUM(total_amount) AS total_sum " \
                    f" FROM (" \
                    f" SELECT total_amount" \
                    f" FROM user_credit_card_transactions" \
                    f" WHERE EXTRACT(MONTH FROM date_of_transaction) = {num_to_month(selected_month)}" \
                    f" AND EXTRACT(YEAR FROM date_of_transaction) =  {selected_year}" \
                    f" AND username = '{username}'"\
                    ") AS subquery; "\

            result = self.__manage_credit_cards_transactions.transaction_query(sql_query=query)
            return format_result(result)

        def how_much_spent_in_specific_date_specific_card(selected_month: Text, selected_year: int, selected_card: int, username: Text):
            query = f"SELECT SUM(total_amount) AS total_sum " \
                    f" FROM (" \
                    f" SELECT total_amount" \
                    f" FROM user_credit_card_transactions" \
                    f" WHERE EXTRACT(MONTH FROM date_of_transaction) = {num_to_month(selected_month)}" \
                    f" AND EXTRACT(YEAR FROM date_of_transaction) =  {selected_year}" \
                    f" AND username = '{username}'" \
                    f" AND last_4_digits = '{selected_card}'" \
                    ") AS subquery;"\

            result = self.__manage_credit_cards_transactions.transaction_query(sql_query=query)
            return format_result(result)

        def how_much_earned_in_specific_date(selected_month: Text, selected_year: int, username: Text):
            query = f"SELECT SUM(income_balance) AS total_sum " \
                    f"FROM (" \
                    f"SELECT income_balance" \
                    f" FROM user_bank_transactions" \
                    f" WHERE EXTRACT(MONTH FROM transaction_date) = {num_to_month(selected_month)}" \
                    f" AND EXTRACT(YEAR FROM transaction_date) =  {selected_year}" \
                    f" AND username='{username}')" \
                    f" AS subquery;"

            result = self.__manage_bank_transactions.transaction_query(sql_query=query)
            return format_result(result)

        def how_much_spent_in_specific_year(selected_year: int, username: Text):
            query = f"SELECT SUM(total_amount) AS total_sum " \
                    f"FROM (" \
                    f"SELECT total_amount" \
                    f" FROM user_credit_card_transactions" \
                    f" WHERE EXTRACT(YEAR FROM date_of_transaction) = {selected_year}" \
                    f" AND username='{username}')" \
                    f" AS subquery;"

            result = self.__manage_credit_cards_transactions.transaction_query(sql_query=query)
            return format_result(result)

        def how_much_spent_in_specific_business(business_name: Text, username: Text):
            query = f"SELECT SUM(total_amount) AS total_sum " \
                    f"FROM (" \
                    f"SELECT total_amount" \
                    f" FROM user_credit_card_transactions" \
                    f" WHERE business_name ILIKE '%{business_name}%'" \
                    f" AND username='{username}')" \
                    f" AS subquery;"

            result = self.__manage_credit_cards_transactions.transaction_query(sql_query=query)
            return format_result(result)

        def which_records_by_transaction_type(transaction_type: Text, username: Text):
            query = f"SELECT * " \
                    f"FROM user_credit_card_transactions" \
                    f" WHERE transaction_type = '{transaction_type}'" \
                    f" AND username='{username}';"

            result = self.__manage_credit_cards_transactions.transaction_query(sql_query=query)
            return format_result(result)

        def which_records_by_business_name(business_name: Text, username: Text):
            query = f"SELECT * " \
                    f"FROM user_credit_card_transactions" \
                    f" WHERE business_name ILIKE '%{business_name}%'" \
                    f" AND username='{username}';"

            result = self.__manage_credit_cards_transactions.transaction_query(sql_query=query)
            return format_result(result)

        def which_records_above_amount(amount: float, username: Text):
            query = f"SELECT * " \
                    f"FROM user_credit_card_transactions" \
                    f" WHERE total_amount >= '{amount}'" \
                    f" AND username='{username}';"

            result = self.__manage_credit_cards_transactions.transaction_query(sql_query=query)
            return format_result(result)

        def which_records_of_transaction_provider(transaction_provider: Text, username: Text):
            query = f"SELECT * " \
                    f"FROM user_credit_card_transactions" \
                    f" WHERE user_credit_card_transactions.transaction_provider ILIKE '%{transaction_provider}%'" \
                    f" AND username='{username}';"

            result = self.__manage_credit_cards_transactions.transaction_query(sql_query=query)
            return format_result(result)

        def how_many_records_from_specific_business(business_name: Text, username: Text):
            query = f"SELECT COUNT(subquery) AS total_transactions " \
                    f"FROM (" \
                    f"SELECT total_amount" \
                    f" FROM user_credit_card_transactions" \
                    f" WHERE business_name ILIKE '%{business_name}%'" \
                    f" AND username='{username}')" \
                    f" AS subquery;"

            result = self.__manage_credit_cards_transactions.transaction_query(sql_query=query)
            return format_result(result)

        def how_much_spent_by_category(username: Text):
            query = f"SELECT transaction_category, SUM(total_amount)" \
                    f" FROM user_credit_card_transactions" \
                    f" WHERE username='{username}'" \
                    f" GROUP BY transaction_category;"

        def how_much_spent_by_category_specific_date(selected_month: Text, selected_year: int, username: Text):
            query = f"SELECT transaction_category, SUM(charge_amount) AS total_category_sum" \
                    f" FROM user_credit_card_transactions" \
                    f" WHERE EXTRACT(MONTH FROM date_of_transaction) = '{num_to_month(selected_month)}'" \
                    f" AND EXTRACT(YEAR FROM date_of_transaction) = '{selected_year}'" \
                    f" AND username='{username}'" \
                    f" GROUP BY transaction_category;"

            result = self.__manage_credit_cards_transactions.transaction_query(sql_query=query)
            return result

        def how_much_spent_by_category_specific_date_card(selected_month: Text, selected_year: int, selected_card: int, username: Text):
            query = f"SELECT transaction_category, SUM(charge_amount) AS total_category_sum" \
                    f" FROM user_credit_card_transactions" \
                    f" WHERE EXTRACT(MONTH FROM date_of_transaction) = '{num_to_month(selected_month)}'" \
                    f" AND EXTRACT(YEAR FROM date_of_transaction) = '{selected_year}'" \
                    f" AND username='{username}'" \
                    f" AND last_4_digits='{selected_card}'" \
                    f" GROUP BY transaction_category;"

            result = self.__manage_credit_cards_transactions.transaction_query(sql_query=query)
            return result

        def total_transaction_amount_by_bank_category(username: Text):
            query = f"SELECT transaction_category, SUM(income_balance)" \
                    f" FROM user_bank_transactions" \
                    f" WHERE username='{username}'" \
                    f" GROUP BY transaction_category;"

            result = self.__manage_bank_transactions.transaction_query(sql_query=query)
            return result

        def how_much_spent_by_card_number(username: Text):
            query = f"SELECT user_credit_card_transactions.last_4_digits, user_cards.issuer_name, SUM(user_credit_card_transactions.total_amount) AS total_amount_sum " \
                    f"FROM user_credit_card_transactions " \
                    f"JOIN user_cards " \
                    f"ON user_credit_card_transactions.last_4_digits = user_cards.last_4_digits " \
                    f"AND user_credit_card_transactions.username = user_cards.username " \
                    f"WHERE user_credit_card_transactions.username = '{username}' " \
                    f"GROUP BY user_credit_card_transactions.last_4_digits, user_cards.issuer_name;"

            result = self.__manage_credit_cards_transactions.transaction_query(sql_query=query)
            return result

        return {
            'how_much_spent_in_specific_date_bank': how_much_spent_in_specific_date_bank,
            'how_much_spent_in_specific_date_card': how_much_spent_in_specific_date_card,
            'how_much_spent_in_specific_date_specific_card': how_much_spent_in_specific_date_specific_card,
            'how_much_spent_by_category_specific_date': how_much_spent_by_category_specific_date,
            'how_much_spent_by_category_specific_date_card': how_much_spent_by_category_specific_date_card,
            'how_much_earned_in_specific_date': how_much_earned_in_specific_date,
            'how_much_spent_in_specific_year': how_much_spent_in_specific_year,
            'how_much_spent_in_specific_business': how_much_spent_in_specific_business,
            'which_records_by_transaction_type': which_records_by_transaction_type,
            'which_records_by_business_name': which_records_by_business_name,
            'which_records_above_amount': which_records_above_amount,
            'which_records_of_transaction_provider': which_records_of_transaction_provider,
            'how_many_records_from_specific_business': how_many_records_from_specific_business,
            'how_much_spent_by_category': how_much_spent_by_category,
            'total_transaction_amount_by_bank_category': total_transaction_amount_by_bank_category,
            'how_much_spent_by_card_number': how_much_spent_by_card_number,
        }


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

    if isinstance(month, int):
        return month