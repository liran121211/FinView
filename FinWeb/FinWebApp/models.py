from datetime import datetime
from typing import Text, List

import pandas as pd
from django.db import models
from . import FIN_CORE, INVALID_ANSWER


def IncomeAgainstOutcome(username: Text):
    # Get the current date
    month, year = datetime.now().month, datetime.now().year

    income_query = FIN_CORE.ask['how_much_earned_in_specific_month'](selected_month=month, selected_year=2023, username=username)
    outcome_query = FIN_CORE.ask['how_much_spent_in_specific_month_bank'](selected_month=month, selected_year=2023, username=username)

    # handle case of missing data from specific date.
    if income_query is None or outcome_query is None:
        return INVALID_ANSWER

    try:
        return (outcome_query / income_query) * 100
    except ZeroDivisionError:
        return INVALID_ANSWER


def IncomeByMonthQuery(username: Text):
    cols_names = ['month_name', 'total_amount', ]
    hebrew_months = ["ינואר", "פבואר", "מרץ", "אפריל", "מאי", "יוני", "יולי", 'אוגוסט', 'ספטמבר', 'אוקטובר', 'נובמבר',
                     'דצמבר']

    income_by_month = []
    for i, _ in enumerate(hebrew_months, start=1):
        query = FIN_CORE.ask['how_much_earned_in_specific_month'](selected_month=i, selected_year=2023, username=username)
        if query is None:
            income_by_month.append(0.)
        else:
            income_by_month.append(query)

    return pd.DataFrame(zip(hebrew_months, income_by_month), columns=cols_names).to_dict()


def SpentByCategoryQuery(username: Text):
    cols_names = ['transaction_category', 'total_amount', ]

    query = FIN_CORE.ask['how_much_spent_by_category'](username=username)
    return pd.DataFrame(query, columns=cols_names).to_dict()


def SpentByMonthQuery(username: Text, dates: List, sort: Text = 'Monthly'):
    cols_names = ['date_of_transaction', 'total_amount', ]
    result = dict()
    for date in dates:
        query = FIN_CORE.ask['how_much_spent_in_specific_month_card'](int(date[0]), int(date[1]), username)
        result['/'.join(date)] = round(query, 2) if query is not None else 0.0

    if sort == 'Monthly':
        return result

    if sort == 'Quarterly':
        # Check if the length of the list is divisible by 3
        if len(result) % 3 != 0:
            return [0.0 for _ in range(12)]

        # List to store the sums of chunks
        quarters_sums = {
            'רבעון 1': 0.0,
            'רבעון 2': 0.0,
            'רבעון 3': 0.0,
            'רבעון 4': 0.0
        }

        # Iterate over the list in chunks of three
        result_vals = [sum(list(result.values())[i:i+3]) for i in range(0, len(result), 3)]
        for i, (k,v) in enumerate(quarters_sums.items()):
            quarters_sums[k] = round(result_vals[i], 2)
        return quarters_sums

    if sort == 'Yearly':
        try:
            extract_years = {x.split('/')[1] for x in result.keys()}
            yearly_sums = {
                extract_years.pop(): 0.0,
                extract_years.pop(): 0.0,
            }

            for current_year in yearly_sums.keys():
                yearly_sums[current_year] = round(sum([v for (k,v) in result.items() if current_year in k]), 2)
        except IndexError:
            return [0.0 for _ in range(12)]
        except ValueError:
            return [0.0 for _ in range(12)]

        return yearly_sums

    # invalid sort selection
    return [0.0 for _ in range(12)]

def BankTransactionByCategoryQuery(username: Text):
    cols_names = ['transaction_category', 'total_amount', ]

    query = FIN_CORE.ask['total_transaction_amount_by_bank_category'](username=username)
    return pd.DataFrame(query, columns=cols_names).to_dict()


def SpentByCardNumberQuery(username: Text):
    cols_names = ['last_4_digits', 'issuer_name', 'total_amount', ]

    query = FIN_CORE.ask['how_much_spent_by_card_number'](username=username)
    return pd.DataFrame(query, columns=cols_names).to_dict()


class UserPersonalInformation(models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=9, db_column='password')
    first_name = models.CharField(max_length=9, db_column='first_name')
    last_name = models.CharField(max_length=9, db_column='last_name')
    email = models.EmailField(max_length=9, db_column='email')
    active_user = models.BooleanField(max_length=9, db_column='is_active')
    date_joined = models.DateField(max_length=9, db_column='date_joined')
    portrait = models.CharField(max_length=100, db_column='portrait')

    class Meta:
        # Specify the table name here
        db_table = 'auth_user'
        app_label = 'FinWeb'  # Specify the app label that doesn't exist in INSTALLED_APPS

    def __str__(self):
        return self.username


class UserFinancialInformation(models.Model):
    username = models.CharField(max_length=50, primary_key=True)
    current_debit = models.FloatField(max_length=9, db_column='current_debit')
    latest_debit = models.FloatField(max_length=9, db_column='latest_debit')
    total_saving = models.FloatField(max_length=9, db_column='total_saving')

    class Meta:
        # Specify the table name here
        db_table = 'user_information'
        app_label = 'FinWeb'  # Specify the app label that doesn't exist in INSTALLED_APPS

    def __str__(self):
        return self.username


class UserCards(models.Model):
    last_4_digits = models.CharField(max_length=4, db_column='last_4_digits')
    card_type = models.CharField(max_length=50, db_column='card_type')
    issuer_name = models.CharField(max_length=50, db_column='issuer_name')
    full_name = models.CharField(max_length=50, db_column='full_name')
    username = models.CharField(max_length=50, db_column='username')
    sha1_identifier = models.CharField(max_length=40, primary_key=True)

    class Meta:
        # Specify the table name here
        db_table = 'user_cards'
        app_label = 'FinWeb'  # Specify the app label that doesn't exist in INSTALLED_APPS

    def __str__(self):
        return self.id

    def to_dict(self):
        # order of dictionary building is crucial for primary key (keep this order)
        return {
            'last_4_digits': self.last_4_digits,
            'card_type': self.card_type,
            'issuer_name': self.issuer_name,
            'full_name': self.full_name,
            'username': self.username,
            'sha1_identifier': self.sha1_identifier
        }


class UserDirectDebitSubscriptions(models.Model):
    sha1_identifier = models.IntegerField(max_length=40, primary_key=True)
    username = models.CharField(max_length=50, db_column='username')
    payment_type = models.CharField(max_length=50, db_column='payment_type')
    amount = models.FloatField(max_length=50, db_column='amount')
    provider_name = models.CharField(max_length=50, db_column='provider_name')

    class Meta:
        # Specify the table name here
        db_table = 'user_direct_debit_subscriptions'
        app_label = 'FinWeb'  # Specify the app label that doesn't exist in INSTALLED_APPS

    def __str__(self):
        return self.id


class UserCreditCardsTransactions(models.Model):
    sha1_identifier = models.CharField(max_length=40, primary_key=True)
    date_of_transaction = models.DateField(max_length=50, db_column='date_of_transaction')
    business_name = models.CharField(max_length=50, db_column='business_name')
    charge_amount = models.FloatField(max_length=50, db_column='charge_amount')
    total_amount = models.FloatField(max_length=50, db_column='total_amount')
    username = models.CharField(max_length=50, db_column='username')
    transaction_provider = models.CharField(max_length=50, db_column='transaction_provider')
    transaction_type = models.CharField(max_length=50, db_column='transaction_type')
    transaction_category = models.CharField(max_length=50, db_column='transaction_category')
    last_4_digits = models.CharField(max_length=4, db_column='last_4_digits')

    class Meta:
        # Specify the table name here
        db_table = 'user_credit_card_transactions'
        app_label = 'FinWeb'  # Specify the app label that doesn't exist in INSTALLED_APPS

    def __str__(self):
        return self.sha1_identifier


class UserBankTransactions(models.Model):
    sha1_identifier = models.CharField(max_length=40, primary_key=True)
    transaction_date = models.DateField(max_length=50, db_column='transaction_date')
    transaction_description = models.CharField(max_length=50, db_column='transaction_description')
    income_balance = models.FloatField(max_length=50, db_column='income_balance')
    outcome_balance = models.FloatField(max_length=50, db_column='outcome_balance')
    current_balance = models.FloatField(max_length=50, db_column='current_balance')
    username = models.CharField(max_length=50, db_column='username')
    transaction_provider = models.CharField(max_length=50, db_column='transaction_provider')
    account_number = models.CharField(max_length=50, db_column='account_number')
    transaction_reference = models.CharField(max_length=50, db_column='transaction_reference')
    transaction_category = models.CharField(max_length=50, db_column='transaction_category')

    class Meta:
        # Specify the table name here
        db_table = 'user_bank_transactions'
        app_label = 'FinWeb'  # Specify the app label that doesn't exist in INSTALLED_APPS

    def __str__(self):
        return self.sha1_identifier
