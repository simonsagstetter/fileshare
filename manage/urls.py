from django.urls import path

from manage.views import (
Login,
Logout
)

app_name = 'manage'

urlpatterns = [
    path('login/', Login.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),
]
