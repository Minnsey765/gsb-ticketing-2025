from django.urls import path

from scanner import views

urlpatterns = [
    path('', views.checkin),
]
