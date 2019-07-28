# _*_coding:utf-8_*_
from django.urls import path
from articles.views import *

app_name = 'articles'

urlpatterns = [
	path('detail/<int:aid>/', article_detail, name='article_detail'),
	path('comment/', comment, name='comment'),
	path('add/', add_article, name='add_article'),
	path('clove/', comment_love, name='comment_love'),
]
