import math
from datetime import datetime
from typing import Text, List
import pandas as pd
from django.db import models
from . import FIN_CORE, INVALID_ANSWER


def IncomeAgainstOutcome(username: Text):
    # Get the current date
    month, year = datetime.now().month, datetime.now().year

    income_query = FIN_CORE.ask['how_much_earned_in_specific_date'](selected_month=month, selected_year=2023, username=username)
    outcome_query = FIN_CORE.ask['how_much_spent_in_specific_date_bank'](selected_month=month, selected_year=2023, username=username)

    # handle case of missing data from specific date.
    if income_query is None or outcome_query is None:
        return INVALID_ANSWER

    try:
        return (outcome_query / income_query) * 100
    except ZeroDivisionError:
        return INVALID_ANSWER


def IncomeByMonthQuery(username: Text):
    cols_names = ['month_name', 'total_amount', ]
    hebrew_months = ["ינואר", "פבואר", "מרץ", "אפריל", "מאי", "יוני", "יולי", 'אוגוסט', 'ספטמבר', 'אוקטובר', 'נובמבר', 'דצמבר']

    income_by_month = []
    for i, _ in enumerate(hebrew_months, start=1):
        query = FIN_CORE.ask['how_much_earned_in_specific_date'](selected_month=i, selected_year=2023, username=username)
        if query is None:
            income_by_month.append(0.)
        else:
            income_by_month.append(query)

    return pd.DataFrame(zip(hebrew_months, income_by_month), columns=cols_names).to_dict()


def SpentByBusinessQuery(username: Text, mode: Text = 'Simple'):
    if mode == 'Simple':
        cols_names = ['transaction_category', 'total_amount', ]

        query = FIN_CORE.ask['which_records_by_business_name'](business_name='', username=username)
        return pd.DataFrame(query, columns=cols_names).to_dict()

    else:
        business_name_query_idx, charge_amount_query_idx = 1, 2
        charge_amount_dict_idx, purchases_quantity_dict_idx = 0, 1
        record_structure = dict()

        query = FIN_CORE.ask['which_records_by_business_name'](business_name='', username=username)
        for record in query:
            if record[business_name_query_idx] in record_structure.keys():
                record_structure[record[business_name_query_idx]][charge_amount_dict_idx] += record[charge_amount_query_idx]
                record_structure[record[business_name_query_idx]][purchases_quantity_dict_idx] += 1
            else:
                record_structure[record[business_name_query_idx]] = [record[charge_amount_query_idx], 1]

        chart_data = []
        for business_name, (charge_amount, num_of_purchases) in record_structure.items():
            data_point = {
                'x': num_of_purchases,  # Average charge amount per merchant (replace if needed)
                'y': round(charge_amount, 2),  # Number of transactions (can be adjusted based on your data)
                'label': business_name
            }
            chart_data.append(data_point)

        return sorted(chart_data, key=lambda x: x['x'], reverse=True)


def spent_by_category_query(username: Text, mode: Text = 'Simple', dates: List = None, sort_period: Text = 'Monthly', sort_card: Text = 'All'):
    cols_names = ['transaction_category', 'total_amount', ]

    if mode == 'Simple':
        query = FIN_CORE.ask['how_much_spent_by_category'](username=username)
        return pd.DataFrame(query, columns=cols_names).to_dict()

    else:
        result = dict()
        for (month, year) in dates:
            if sort_card == 'All':
                query = FIN_CORE.ask['how_much_spent_by_category_specific_date'](month, year, username)
            else:
                query = FIN_CORE.ask['how_much_spent_by_category_specific_date_card'](month, year, int(sort_card), username)

            date_yo_string = str(month) + '/' + str(year)
            if len(query) == 0:
                result[date_yo_string] = []

            for (category, charge_amount) in query:
                record_charge_amount = round(float(charge_amount), 2)
                record_category = category

                if date_yo_string not in result.keys():
                    result[date_yo_string] = [[record_category, record_charge_amount]]
                else:
                    result[date_yo_string].append([record_category, charge_amount])

        if sort_period == 'Monthly':
            return result

        if sort_period == 'Quarterly':
            QUARTER_1, QUARTER_2, QUARTER_3, QUARTER_4 = 2, 5, 8, 11
            # Check if the length of the list is divisible by 3
            if len(result) % 3 != 0:
                for date_yo_string, categories_list in result.items():
                    for idx, (category, charge_amount) in enumerate(categories_list):
                        result[date_yo_string][idx] = [0.0, category]

            quarter_categories  = dict()
            quarters_sums       = dict()
            for idx, (date_yo_string, categories_list) in enumerate(result.items()):
                if idx % 3 == 0:
                    quarter_categories = dict()

                for category, charge_amount in categories_list:
                    if category not in quarter_categories.keys():
                        quarter_categories[category] = charge_amount
                    else:
                        quarter_categories[category] += charge_amount

                # List to store the sums of chunks
                if idx == QUARTER_1:
                    quarters_sums['רבעון 1'] = [[k,v] for k,v in quarter_categories.items()]
                if idx == QUARTER_2:
                    quarters_sums['רבעון 2'] = [[k,v] for k,v in quarter_categories.items()]
                if idx == QUARTER_3:
                    quarters_sums['רבעון 3'] = [[k,v] for k,v in quarter_categories.items()]
                if idx == QUARTER_4:
                    quarters_sums['רבעון 4'] = [[k,v] for k,v in quarter_categories.items()]

            return quarters_sums

        if sort_period == 'Yearly':
            try:
                yearly_sums = dict()
                extract_years = {x.split('/')[1] for x in result.keys()}

                for year in extract_years:
                    year_categories = dict()

                    for idx, (date_yo_string, categories_list) in enumerate(result.items()):
                        if year in date_yo_string:

                            for category, charge_amount in categories_list:
                                if category not in year_categories.keys():
                                    year_categories[category] = charge_amount
                                else:
                                    year_categories[category] += charge_amount

                    # List to store the sums of chunks
                    yearly_sums[year] = [[k,v] for k,v in year_categories.items()]

            except IndexError:
                extract_years = {x.split('/')[1] for x in result.keys()}
                err_result = dict()

                for year in extract_years:
                    err_result[year] = [[]]
                return err_result

            except ValueError:
                extract_years = {x.split('/')[1] for x in result.keys()}
                err_result = dict()

                for year in extract_years:
                    err_result[year] = [[]]
                return err_result

            return yearly_sums


def spent_by_date_query(username: Text, dates: List, sort_period: Text = 'Monthly', sort_card: Text = 'All'):
    result = dict()
    for (month, year) in dates:
        if sort_card == 'All':
            query = FIN_CORE.ask['how_much_spent_in_specific_date_card'](month, year, username)
            result[str(month) + '/' + str(year)] = round(query, 2) if query is not None else 0.0
        else:
            query = FIN_CORE.ask['how_much_spent_in_specific_date_specific_card'](month, year, int(sort_card), username)
            result[str(month) + '/' + str(year)] = round(query, 2) if query is not None else 0.0

    if sort_period == 'Monthly':
        return result

    if sort_period == 'Quarterly':
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

    if sort_period == 'Yearly':
        try:
            extract_years = {x.split('/')[1] for x in result.keys()}
            yearly_sums = dict()
            for year in extract_years:
                yearly_sums[year] = 0.0

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
