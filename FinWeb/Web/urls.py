"""
URL configuration for FinWeb project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import os

from django.contrib import admin
from django.urls import path
from FinWebApp.views import login_view, home_view, settings_view, settings_personal_information_post, settings_user_cards_post, register_post, login_post, logout_view, upload_post, analytics_and_trends_view

urlpatterns = [
    path('', home_view, name='home_page'),
    path('admin/', admin.site.urls),
    path('login/', login_view, name='login_page'),
    path('logout/', logout_view, name='logout_page'),
    path('settings/', settings_view, name='settings_page'),
    path('analytics_and_trends/', analytics_and_trends_view, name='analytics_and_trends_page'),


    # post paths
    path('settings/submit_personal_information', settings_personal_information_post, name='settings_personal_information_post'),
    path('settings/submit_user_cards', settings_user_cards_post, name='settings_user_cards_post'),
    path('settings/upload', upload_post, name='upload_post'),
    path('login/signup', register_post, name='register_post'),
    path('login/authenticate', login_post, name='login_post'),
]

handler404 = 'FinWebApp.views.handler404'
