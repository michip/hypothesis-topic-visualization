from django.contrib import admin
from django.urls import path
from .views import home, topic

urlpatterns = [
    path('', home),
    path('topic/<int:id>', topic),
]
