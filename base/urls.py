from django.urls import path
from .views import *

app_name = 'base'
urlpatterns = [
    path('', index, name='index'),
    path('news/<str:lang>/<str:username>', MainPage.as_view(), name='main_page'),
    path('news/<str:lang>/<int:news_id>/<str:username>/comments', comments_view, name='comments'),
    path('save_news/<str:lang>/<int:news_id>/<str:username>', save_news, name='save_news'),
    path('news/login', user_login, name='login'),
    path('news/<str:lang>/register/', register_user, name='register'),
    path('news/<str:lang>/logout/', user_logout, name='logout'),

]
# RegisterUser.as_view()