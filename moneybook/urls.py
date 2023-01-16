from django.urls import path
from . import views

urlpatterns = [
    path("", views.MoneyBookLogAPIView.as_view(), name="moneybook_log"),
]
