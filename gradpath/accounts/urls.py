from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import home_view, signup_view, login_view, logout_view, welcome_view, account_settings

urlpatterns = [
    path('', home_view, name='home'),
    path('signup/', signup_view, name='signup'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('welcome/', welcome_view, name='welcome'),
    path('account-settings/', account_settings, name='account_settings'),
]
