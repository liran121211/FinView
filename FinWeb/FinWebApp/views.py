from typing import Text
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect

from FinWeb.FinWebApp.models import UserInformation, UserCards


def home_view(request):
    logged_in_user = 'liran121214'
    # pie_chart_data = model_payment_provider_pie_chart(username='liran1214')
    # pie_chart_labels = list(pie_chart_data.keys())
    # pie_chart_values = list(pie_chart_data)

    return render(request, 'home.html', {
        'user_information': retrieve_user_information(logged_in_user),
        'user_cards': retrieve_user_cards(logged_in_user)
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
