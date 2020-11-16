from django.contrib import admin
from django.urls import path
from .views import home, topic, topic_overview, configuration, search, imprint

urlpatterns = [
    path('', home, name="home"),
    path('imprint', imprint, name="imprint"),
    path('topic/<int:id>', topic, name="topic"),
    path('configuration', configuration, name="configuration"),
    path('topics', topic_overview, name="topic-overview"),
    path('search', search, name="search"),
]
