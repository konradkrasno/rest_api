from django.urls import path

from . import views

app_name = "api"

urlpatterns = [
    path("zadanie1/", views.process_names, name="zadanie1"),
    path("zadanie2/", views.calculate_price, name="zadanie2"),
]
