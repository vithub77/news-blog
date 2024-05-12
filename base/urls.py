from django.urls import path
from .views import *

app_name = 'base'
urlpatterns = [
    path('', index, name='index'),
    path('news/<str:lang>/', page_news, name='page_news'),
]
