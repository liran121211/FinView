from typing import Text

import pandas as pd
from django.db import models
from . import finview_app


# Create your models here.

def model_payment_provider_pie_chart(username: Text):
    cols_name_chronology = ['date_of_purchase', 'business_name', 'charge_amount', 'payment_type',
                            'total_amount', 'sha1_identifier', 'username', 'payment_provider']

    query = finview_app.ask['which_records_of_payment_provider'](payment_provider='', username=username)
    return pd.DataFrame(query, columns=cols_name_chronology).groupby('payment_provider')['total_amount'].sum()


class UserInformation(models.Model):
    username = models.CharField(max_length=20, primary_key=True)
    current_debit = models.FloatField(db_column='current_debit')
    latest_debit = models.FloatField(db_column='latest_debit')
    total_saving = models.FloatField(db_column='total_saving')

    class Meta:
        # Specify the table name here
        db_table = 'user_information'
        app_label = 'FinWeb'  # Specify the app label that doesn't exist in INSTALLED_APPS

    def __str__(self):
        return self.username


class UserCards(models.Model):
    id = models.IntegerField(max_length=6, primary_key=True)
    username = models.CharField(max_length=20, db_column='username')
    issuer_name = models.CharField(max_length=20, db_column='issuer_name')
    last_four_digits = models.IntegerField(max_length=4, db_column='last_four_digits')
    card_type = models.CharField(max_length=10, db_column='card_type')
    full_name = models.CharField(max_length=20, db_column='full_name')

    class Meta:
        # Specify the table name here
        db_table = 'user_cards'
        app_label = 'FinWeb'  # Specify the app label that doesn't exist in INSTALLED_APPS

    def __str__(self):
        return self.id


class UserPaymentRecords(models.Model):
    id = models.IntegerField(max_length=6, primary_key=True)
    username = models.CharField(max_length=20, db_column='username')
    payment_type = models.CharField(max_length=20, db_column='payment_type')
    amount = models.FloatField(max_length=20, db_column='amount')
    provider_name = models.CharField(max_length=20, db_column='provider_name')

    class Meta:
        # Specify the table name here
        db_table = 'user_payment_records'
        app_label = 'FinWeb'  # Specify the app label that doesn't exist in INSTALLED_APPS

    def __str__(self):
        return self.id


class UserTransactions(models.Model):
    sha1_identifier = models.CharField(max_length=300, primary_key=True)
    date_of_transaction = models.DateField(max_length=20, db_column='date_of_transaction')
    business_name = models.CharField(max_length=20, db_column='business_name')
    charge_amount = models.FloatField(max_length=20, db_column='charge_amount')
    payment_type = models.CharField(max_length=20, db_column='payment_type')
    total_amount = models.FloatField(max_length=20, db_column='total_amount')
    username = models.CharField(max_length=20, db_column='username')
    payment_provider = models.CharField(max_length=20, db_column='payment_provider')
    transaction_type = models.CharField(max_length=20, db_column='transaction_type')
    category = models.CharField(max_length=20, db_column='category')

    class Meta:
        # Specify the table name here
        db_table = 'user_transactions'
        app_label = 'FinWeb'  # Specify the app label that doesn't exist in INSTALLED_APPS

    def __str__(self):
        return self.sha1_identifier

