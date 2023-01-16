from django.urls import path
from . import views

urlpatterns = [
    path("", views.MoneyBookLogAPIView.as_view(), name="moneybook_log"),
    path("<int:log_id>/", views.MoneyBookLogDetailAPIView.as_view(), name="detail_log"),
]
