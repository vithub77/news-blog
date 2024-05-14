from django.urls import path
from .views import *

app_name = 'base'
urlpatterns = [
    path('', index, name='index'),
    path('news/<str:lang>/', MainPage.as_view(), name='main_page'),
    path('news/<str:lang>/username', Login.as_view(), name='login'),
    path('news/<str:lang>/register/', Register.as_view(), name='register'),
]
