from typing import Text
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect

from FinWeb.FinWebApp.models import UserInformation, UserCards, UserDirectDebitSubscriptions, UserBankTransactions, \
    SpentByCategoryQuery, SpentByCardNumberQuery, IncomeByMonthQuery, UserCreditCardsTransactions


def home_view(request):
    logged_in_user = 'liran121214'

    return render(request, 'home.html', {
        'user_information': retrieve_user_information(logged_in_user),
        'user_cards': retrieve_user_cards(logged_in_user),
        'user_direct_debit_subscriptions': retrieve_user_direct_debit_subscription_records(logged_in_user),
        'user_income': slice_dictionary(retrieve_user_bank_transactions(logged_in_user), -5, 0),
        'user_outcome': slice_dictionary(retrieve_user_credit_card_transactions(logged_in_user), -5, 0),
        'spent_by_category': SpentByCategoryQuery(logged_in_user),
        'spent_by_card': SpentByCardNumberQuery(logged_in_user),
        'income_by_month': IncomeByMonthQuery(logged_in_user)
    })


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('..', {'data': 'Login Successfully'})
        else:
            return render(request, 'login.html', {'data': 'Invalid username or password'})

    return render(request, 'login.html', )


def retrieve_user_information(username: Text) -> dict:
    # Retrieve all rows from the table
    filtered_data = UserInformation.objects.filter(username=username).first()

    if filtered_data is None:
        filtered_data = {
            'latest_debit': 0.0,
            'current_debit': 0.0,
            'total_saving': 0.0
        }

    return {
        'latest_debit': filtered_data.latest_debit,
        'current_debit': filtered_data.current_debit,
        'total_saving': filtered_data.total_saving,
    }


def retrieve_user_cards(username: Text) -> dict:
    # Retrieve all rows from the table
    filtered_data = UserCards.objects.filter(username=username).all()

    if filtered_data is None:
        filtered_data = {
            'issuer_name': [],
            'last_4_digits': [],
            'card_type': [],
            'full_name': [],
        }
        return filtered_data

    dict_data = dict()
    for data in filtered_data:
        if dict_data.get('issuer_name', None) is None:
            dict_data['issuer_name'] = [data.issuer_name]
        else:
            dict_data['issuer_name'].append(data.issuer_name)

        if dict_data.get('last_4_digits', None) is None:
            dict_data['last_4_digits'] = [data.last_4_digits]
        else:
            dict_data['last_4_digits'].append(data.last_4_digits)

        if dict_data.get('card_type', None) is None:
            dict_data['card_type'] = [data.card_type]
        else:
            dict_data['card_type'].append(data.card_type)

        if dict_data.get('full_name', None) is None:
            dict_data['full_name'] = [data.full_name]
        else:
            dict_data['full_name'].append(data.full_name)

    return dict_data


def retrieve_user_direct_debit_subscription_records(username: Text) -> dict:
    # Retrieve all rows from the table
    filtered_data = UserDirectDebitSubscriptions.objects.filter(username=username).all()

    if filtered_data is None:
        filtered_data = {
            'payment_type': [],
            'amount': [],
            'provider_name': [],
        }
        return filtered_data

    dict_data = dict()
    for data in filtered_data:
        if dict_data.get('payment_type', None) is None:
            dict_data['payment_type'] = [data.payment_type]
        else:
            dict_data['payment_type'].append(data.payment_type)

        if dict_data.get('amount', None) is None:
            dict_data['amount'] = [data.amount]
        else:
            dict_data['amount'].append(data.amount)

        if dict_data.get('provider_name', None) is None:
            dict_data['provider_name'] = [data.provider_name]
        else:
            dict_data['provider_name'].append(data.provider_name)

    return dict_data


def retrieve_user_credit_card_transactions(username: Text) -> dict:
    # Retrieve all rows from the table
    filtered_data = UserCreditCardsTransactions.objects.filter(username=username).all()

    if filtered_data is None:
        filtered_data = {
            'sha1_identifier': [],
            'date_of_transaction': [],
            'business_name': [],
            'charge_amount': [],
            'total_amount': [],
            'username': [],
            'transaction_provider': [],
            'transaction_type': [],
            'category': [],
            'last_4_digits': [],
        }
        return filtered_data

    dict_data = dict()
    for data in filtered_data:
        if dict_data.get('sha1_identifier', None) is None:
            dict_data['sha1_identifier'] = [data.sha1_identifier]
        else:
            dict_data['sha1_identifier'].append(data.sha1_identifier)

        if dict_data.get('date_of_transaction', None) is None:
            dict_data['date_of_transaction'] = [str(data.date_of_transaction)]
        else:
            dict_data['date_of_transaction'].append(str(data.date_of_transaction))

        if dict_data.get('business_name', None) is None:
            dict_data['business_name'] = [data.business_name]
        else:
            dict_data['business_name'].append(data.business_name)

        if dict_data.get('charge_amount', None) is None:
            dict_data['charge_amount'] = [data.charge_amount]
        else:
            dict_data['charge_amount'].append(data.charge_amount)

        if dict_data.get('total_amount', None) is None:
            dict_data['total_amount'] = [data.total_amount]
        else:
            dict_data['total_amount'].append(data.total_amount)

        if dict_data.get('username', None) is None:
            dict_data['username'] = [data.username]
        else:
            dict_data['username'].append(data.username)

        if dict_data.get('transaction_provider', None) is None:
            dict_data['transaction_provider'] = [data.transaction_provider]
        else:
            dict_data['transaction_provider'].append(data.transaction_provider)

        if dict_data.get('transaction_type', None) is None:
            dict_data['transaction_type'] = [data.transaction_type]
        else:
            dict_data['transaction_type'].append(data.transaction_type)

        if dict_data.get('category', None) is None:
            dict_data['category'] = [data.category]
        else:
            dict_data['category'].append(data.category)

        if dict_data.get('last_4_digits', None) is None:
            dict_data['last_4_digits'] = [data.category]
        else:
            dict_data['last_4_digits'].append(data.category)

    return dict_data

def retrieve_user_bank_transactions(username: Text) -> dict:
    # Retrieve all rows from the table
    filtered_data = UserBankTransactions.objects.filter(username=username).all()

    if filtered_data is None:
        filtered_data = {
            'sha1_identifier': [],
            'transaction_date': [],
            'transaction_description': [],
            'income_balance': [],
            'outcome_balance': [],
            'current_balance': [],
            'username': [],
            'transaction_provider': [],
            'account_number': [],
            'transaction_reference': [],
        }
        return filtered_data

    dict_data = dict()
    for data in filtered_data:
        if dict_data.get('sha1_identifier', None) is None:
            dict_data['sha1_identifier'] = [data.sha1_identifier]
        else:
            dict_data['sha1_identifier'].append(data.sha1_identifier)

        if dict_data.get('transaction_date', None) is None:
            dict_data['transaction_date'] = [str(data.transaction_date)]
        else:
            dict_data['transaction_date'].append(str(data.transaction_date))

        if dict_data.get('transaction_description', None) is None:
            dict_data['transaction_description'] = [data.transaction_description]
        else:
            dict_data['transaction_description'].append(data.transaction_description)

        if dict_data.get('income_balance', None) is None:
            dict_data['income_balance'] = [data.income_balance]
        else:
            dict_data['income_balance'].append(data.income_balance)

        if dict_data.get('outcome_balance', None) is None:
            dict_data['outcome_balance'] = [data.outcome_balance]
        else:
            dict_data['outcome_balance'].append(data.outcome_balance)

        if dict_data.get('current_balance', None) is None:
            dict_data['current_balance'] = [data.current_balance]
        else:
            dict_data['current_balance'].append(data.current_balance)

        if dict_data.get('username', None) is None:
            dict_data['username'] = [data.username]
        else:
            dict_data['username'].append(data.username)

        if dict_data.get('transaction_provider', None) is None:
            dict_data['transaction_provider'] = [data.transaction_provider]
        else:
            dict_data['transaction_provider'].append(data.transaction_provider)

        if dict_data.get('account_number', None) is None:
            dict_data['account_number'] = [data.account_number]
        else:
            dict_data['account_number'].append(data.account_number)

        if dict_data.get('transaction_reference', None) is None:
            dict_data['transaction_reference'] = [data.transaction_reference]
        else:
            dict_data['transaction_reference'].append(data.transaction_reference)

    return dict_data


def slice_dictionary(obj: dict, start_idx: int = 0, end_idx: int = -1) -> dict:
    temp_dict = dict()
    matched_indexes = list()

    # if column == 'all' or keyword == 'all':
    #     matched_indexes = [i for i in range(len(obj.items()))]
    # else:
    #     for k, v in obj.items():
    #         if k == column:
    #             for i, value in enumerate(v):
    #                 if value == keyword:
    #                     matched_indexes.append(i)

    if not start_idx > len(matched_indexes) or not end_idx > len(matched_indexes):
        # if end index is not defined.
        if end_idx == 0:
            matched_indexes = matched_indexes[start_idx:]
        else:
            matched_indexes = matched_indexes[start_idx:end_idx]

    for k, v in obj.items():
        for i, value in enumerate(v):
            if i in matched_indexes:
                if k not in temp_dict.keys():
                    temp_dict[k] = [value]
                else:
                    temp_dict[k].append(value)

    return temp_dict
