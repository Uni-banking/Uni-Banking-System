from django.urls import path
from account import views

app_name = "account"

urlpatterns = [
    path("", views.AccountView, name="account"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("unibank-reg/", views.unibank_registration, name="Unibank-reg"),
]
