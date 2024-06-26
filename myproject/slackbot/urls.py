from django.urls import path
from . import views

urlpatterns = [
    path('events/', views.slack_events, name='slack_events'),
]
