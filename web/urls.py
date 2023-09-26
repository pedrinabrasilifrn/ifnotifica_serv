from django.urls import path, include
from django.contrib.auth.models import User
from web import views

app_name="web"
urlpatterns=[
    path('', views.index),
    path('sobre/', views.sobre),
]