from django.shortcuts import render
from django.contrib.auth.views import LoginView, LogoutView

from manage.forms import LoginForm

class Login(LoginView):
    template_name = 'manage/login.html'
    form_class = LoginForm

class Logout(LogoutView):
    template_name = 'manage/logout.html'
