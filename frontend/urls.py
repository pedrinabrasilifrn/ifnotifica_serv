from django.urls import path, include
from django.contrib.auth.models import User
from frontend import views

urlpatterns=[
  path('', views.index),
  path('/api/', include('api.urls'), name='api')
]