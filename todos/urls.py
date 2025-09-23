from . import views
from django.urls import path

urlpatterns = [
    path('home',views.home,name='home'),
    path('register',views.register,name='register'),
    path('login',views.login,name='todo')
]

