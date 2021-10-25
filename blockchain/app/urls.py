from django.contrib import admin
from django.urls import path, include
from .views import Index, SignUp, UserLogin, UserLogout, dashboard, profile


app_name = 'website'


urlpatterns = [
    path('', Index.as_view(), name='index'),
    path('signup/', SignUp.as_view(), name='signup'),
    path('login/', UserLogin.as_view(), name='login'),
    path('logout/', UserLogout.as_view(), name='logout'),
    path('dashboard/', dashboard, name='dashboard'),
    path('dashboard/profile/', profile, name='profile'),
]

