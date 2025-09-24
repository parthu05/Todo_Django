from . import views
from django.urls import path

urlpatterns = [
    path('home',views.home,name='home'),
    path('register',views.register,name='register'),
    path('login',views.login_view,name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('delete-task/<str:name>/', views.DeleteTask, name='delete'),
]

