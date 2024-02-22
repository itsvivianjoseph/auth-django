from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('login', views.login),
    path('signup',views.signup),
    path('test-token',views.test_token)
]