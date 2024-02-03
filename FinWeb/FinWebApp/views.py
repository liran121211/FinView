from typing import Text
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect

from FinWeb.FinWebApp.models import UserInformation, UserCards, UserPaymentRecords, UserTransactions


def home_view(request):
    logged_in_user = 'liran121214'
    # pie_chart_data = model_payment_provider_pie_chart(username='liran1214')
    # pie_chart_labels = list(pie_chart_data.keys())
    # pie_chart_values = list(pie_chart_data)

    return render(request, 'home.html', {
        'user_information': retrieve_user_information(logged_in_user),
        'user_cards': retrieve_user_cards(logged_in_user),
        'user_payment_records': retrieve_user_payment_records(logged_in_user),
        'user_transactions': retrieve_user_transactions(logged_in_user),
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
            'last_four_digits': [],
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

        if dict_data.get('last_four_digits', None) is None:
            dict_data['last_four_digits'] = [data.last_four_digits]
        else:
            dict_data['last_four_digits'].append(data.last_four_digits)

        if dict_data.get('card_type', None) is None:
            dict_data['card_type'] = [data.card_type]
        else:
            dict_data['card_type'].append(data.card_type)

        if dict_data.get('full_name', None) is None:
            dict_data['full_name'] = [data.full_name]
        else:
            dict_data['full_name'].append(data.full_name)

    return dict_data


def retrieve_user_payment_records(username: Text) -> dict:
    # Retrieve all rows from the table
    filtered_data = UserPaymentRecords.objects.filter(username=username).all()

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


def retrieve_user_transactions(username: Text) -> dict:
    # Retrieve all rows from the table
    filtered_data = UserTransactions.objects.filter(username=username).all()

    if filtered_data is None:
        filtered_data = {
            'sha1_identifier': [],
            'date_of_transaction': [],
            'business_name': [],
            'charge_amount': [],
            'payment_type': [],
            'total_amount': [],
            'username': [],
            'payment_provider': [],
            'transaction_type': [],
            'category': [],
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

        if dict_data.get('payment_type', None) is None:
            dict_data['payment_type'] = [data.payment_type]
        else:
            dict_data['payment_type'].append(data.payment_type)

        if dict_data.get('total_amount', None) is None:
            dict_data['total_amount'] = [data.total_amount]
        else:
            dict_data['total_amount'].append(data.total_amount)

        if dict_data.get('username', None) is None:
            dict_data['username'] = [data.username]
        else:
            dict_data['username'].append(data.username)

        if dict_data.get('payment_provider', None) is None:
            dict_data['payment_provider'] = [data.payment_provider]
        else:
            dict_data['payment_provider'].append(data.payment_provider)

        if dict_data.get('transaction_type', None) is None:
            dict_data['transaction_type'] = [data.transaction_type]
        else:
            dict_data['transaction_type'].append(data.transaction_type)

        if dict_data.get('category', None) is None:
            dict_data['category'] = [data.category]
        else:
            dict_data['category'].append(data.category)

    return dict_data

