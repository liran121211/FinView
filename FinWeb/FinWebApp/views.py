from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http import JsonResponse
from chartjs.views.lines import BaseLineChartView

from FinWeb.FinWebApp.models import model_payment_provider_pie_chart


def home_view(request):
    pie_chart_data = model_payment_provider_pie_chart(username='liran')
    pie_chart_labels = list(pie_chart_data.keys())
    pie_chart_values = list(pie_chart_data)
    return render(request, 'home.html', {'labels': pie_chart_labels, 'data': pie_chart_values})


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
