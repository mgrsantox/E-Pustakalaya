from django.urls import path
from .views import category_home

urlpatterns=[
    path('', category_home),
]