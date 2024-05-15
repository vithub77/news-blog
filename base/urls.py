from django.urls import path
from .views import *

app_name = 'base'
urlpatterns = [
    path('', index, name='index'),
    path('news/<str:lang>/<str:username>', MainPage.as_view(), name='main_page'),
    path('news/login', user_login, name='login'),
    path('news/<str:lang>/register/', register_user, name='register'),
    path('news/<str:lang>/logout/', user_logout, name='logout'),

]
# RegisterUser.as_view()