# _*_coding:utf-8_*_
from django.urls import path
from .views import *

app_name = 'users'

urlpatterns = [
	path('register/', register, name='register'),
	path('login/', user_login, name='login'),
	path('logout/', user_logout, name='userlogout')

]
