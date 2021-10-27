from django.contrib import admin
from django.urls import path, include
from .views import (
    Index, SignUp, UserLogin, UserLogout, dashboard, profile, about, blog_detail, contact, 
    add_to_watch,watchlist, purchase,
     ProposalView, UserKycView, AccountView, ProfileView, BlogsView, CurrenciesView
    )


app_name = 'website'


urlpatterns = [
    path('', Index.as_view(), name='index'),
    path('signup/', SignUp.as_view(), name='signup'),
    path('login/', UserLogin.as_view(), name='login'),
    path('logout/', UserLogout.as_view(), name='logout'),
    path('dashboard/', dashboard, name='dashboard'),
    path('about/', about, name='about'),
    path('contact/', contact, name='contact'),
    path('dashboard/account/', AccountView.as_view(), name='account'),
    path('dashboard/profile/', ProfileView.as_view(), name='profile'),
    path('dashboard/kyc/', UserKycView.as_view(), name='userkyc'),
    path('proposal/', ProposalView.as_view(), name='proposal'),
    path('tutorials/', BlogsView.as_view(), name='tutorials'),
    path('tutorials/<int:pk>/', blog_detail, name='tutorial-detail'),

    
    path('crypto/', CurrenciesView.as_view(), name='cryptos'),
    path('add/watch/list/<int:pk>/', add_to_watch, name='add_to_watch'),
    path('watch/list/', watchlist, name='watchlist'),
    path('purchase/<int:pk>/', purchase, name='purchase'),
    # path('purchase/<int:pk>/', PurchaseView.as_view(), name='purchase'),
]

