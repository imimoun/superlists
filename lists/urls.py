from django.urls import path
from superlists.lists import views

urlpatterns = [
    path('', views.home_page),
]
