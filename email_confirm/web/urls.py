from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name = "home"),
    path('signup/', views.signup, name = "signup"),
    path('<url>/activeRegistration', views.activeRegistration, name = "activeRegistration"),
]
